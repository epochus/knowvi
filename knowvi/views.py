from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    # Request context of the request
    # The context contains information such as the client's machine
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine
    context_dict = {'boldmessage': "I am bold font from the context"}
    
    # Return a rendered response to send to the client
    return render_to_response('knowvi/index.html', context_dict, context)

def about(request):
    return HttpResponse('''
        Knowvi Says: Here is the about page. <br/>
        <a href='/knowvi/'>Index</a>
    ''')
