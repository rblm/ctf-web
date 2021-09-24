from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import DlForm

import os
import subprocess
import mimetypes
from django.http import HttpResponse


def enczip(filename='',pw='',pin=''):
    print("f2: "+filename, pw, pin)
    if filename !='':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        basename=filename
        filepath = BASE_DIR + '/dl/files/' + filename+'.txt'
        rc = subprocess.call(['7z', 'a', '-p'+pw, '-y', basename+'.zip', filename+'.txt'], cwd=BASE_DIR+'/dl/files/')
        rc = subprocess.call(['7z', 'a', '-p'+pin, '-y', basename+'-tfa.zip', filename+'.zip'], cwd=BASE_DIR+'/dl/files/')

def download(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            pw=form.cleaned_data.get("password")
            pin=form.cleaned_data.get("pin")
            fname=form.cleaned_data.get("files")
            enczip(fname, pw, pin)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = BASE_DIR + '/dl/files/' + fname+'-tfa.zip'
            # Open the file for reading content
            path = open(filepath, 'rb')
            # Set the mime type
            mime_type, _ = mimetypes.guess_type(filepath)
            #mime_type = "application/zip"
            print(mime_type)
            # Set the return value of the HttpResponse
            response = HttpResponse(path, content_type=mime_type)
            # Set the HTTP header for sending to browser
            response['Content-Disposition'] = "attachment; filename=%s" % fname+'-tfa.zip'
            # Return the response value
            return response
            #return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DlForm()

    return render(request, 'dl.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html')
