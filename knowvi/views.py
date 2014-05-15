from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# import Models
from knowvi.models import Category, Page

# import Forms
from knowvi.forms import CategoryForm
from knowvi.forms import PageForm

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    # Request context of the request
    # The context contains information such as the client's machine
    context = RequestContext(request)

    context_dict = {}

    # Retrieve top 5 categories ranked by likes, descending
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    for category in category_list:
        category.url = encode_url(category.name);
    
    # Return a rendered response to send to the client
    return render_to_response('knowvi/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "I am bold font from the context"}

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

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('knowvi/add_category.html', {'form': form}, context)

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
