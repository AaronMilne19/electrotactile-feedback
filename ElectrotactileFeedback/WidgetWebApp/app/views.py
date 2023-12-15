"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .forms import MainForm
from .helpers import *

#Render the home page
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    form = MainForm()
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'form':form,
        }
    )

#Trigger the device from ajax request
def trigger(request):
    if request.method == "POST":
        widget_type = request.POST.get("widgetType")
        pulsewidth, frequency, amplitude = lookup_widget_parameters(widget_type)
        send_pulse(pulsewidth, frequency, amplitude)
        return JsonResponse({'success': 'true', 'value': 1})
    
    return JsonResponse({'success': 'false'})


#def contact(request):
#    """Renders the contact page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/contact.html',
#        {
#            'title':'Contact',
#            'message':'Your contact page.',
#            'year':datetime.now().year,
#        }
#    )

#def about(request):
#    """Renders the about page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/about.html',
#        {
#            'title':'About',
#            'message':'Your application description page.',
#            'year':datetime.now().year,
#        }
#    )
