from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# import Models
from knowvi.models import Category, Page

# import Forms
from knowvi.forms import CategoryForm
from knowvi.forms import PageForm
from knowvi.forms import UserForm, UserProfileForm

# Checking date and time
from datetime import datetime

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    # Request context of the request
    # The context contains information such as the client's machine
    context = RequestContext(request)
    context_dict = {}

    # Retrieve top 5 categories ranked by views, descending
    category_list = Category.objects.order_by('-views')[:5]
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    for category in category_list:
        category.url = encode_url(category.name);
    
    response = render_to_response('knowvi/index.html', context_dict, context)

    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:7],
            "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
        else:
            # The get returns None, and the session does not have a value for
            # the last visit.
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = 1

    # Return response back to the user, updating any cookies that need changed.
    return response

def about(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "I am bold font from the context"}

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict['visits'] = count

    return render_to_response('knowvi/about.html', context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name}
    context_dict['category_name_url'] = category_name_url

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('knowvi/category.html', context_dict, context)

def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    context_dict = {}

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    context_dict['form'] = form
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('knowvi/add_category.html', context_dict, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    context_dict = {}

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away
            # Not all fields are automatically populated
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the 
                # the category does not exist.
                return render_to_response('knowvi/add_category.html', {}, context)

            # Also, create a default value for the number of views
            page.views = 0

            # With this, we can save our new model instance
            page.save()

            # Now that the page is saved, display the category instead
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict['category_name_url'] = category_name_url
    context_dict['category_name'] = category_name
    context_dict['form'] = form

    return render_to_response('knowvi/add_page.html',
                              context_dict, context)

def register(request):
    # Like before, get the request's context/
    context = RequestContext(request)
    context_dict = {}

    # A boolean value for telling the template whether the registration was 
    # successful. Set to False intially. Code changes value to True when 
    # registration succeeds
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we has the password with the set_password method
            #Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance
            # Since we need to set the user attribute ourselves, we set commit=False
            # This delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put in in the
            # UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to tell the template registration was successful
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal
        # They'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances
    # These forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered

    # Render the template depending on the context
    return render_to_response('knowvi/register.html', context_dict, context)

def user_login(request):
    # Like before, obtain the context for the user's request
    context = RequestContext(request)
    context_dict = {}

    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is retruned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no
        # user with matching credentials was found
        if user:
            # Is the account active? It could haev been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/knowvi/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Knowvi account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the 
        # blank dictionary object...
        return render_to_response('knowvi/login.html', context_dict, context)

@login_required
def restricted(request):
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('knowvi/restricted.html', context_dict, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/knowvi/')

def get_category_list():
    cat_list = Category.objects.all()

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list

def search(request):
    context = RequestContext(request)

    context_dict = {}
    pages = []
    query = ''

    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        pages = Page.objects.filter(title__icontains=query)

    context_dict['query'] = query
    context_dict['pages'] = pages

    return render_to_response('knowvi/search.html', context_dict, context)

def track_url(request):
    context = RequestContext(request)
    page_id = None
    cat_id =  None
    url = '/knowvi/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

def contact(request):
    # Like before, obtain the context for the user's request
    context = RequestContext(request)
    context_dict = {}

    return render_to_response('knowvi/contact.html', context_dict, context)

