from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

import os
import subprocess
import mimetypes
from django.http import HttpResponse



from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    CredentialPromptForm,
    CredsInputForm,
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm
)


def download(request,filename=''):
    print("f2: "+filename)
    if filename !='':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        basename=filename.split('.')[0]
        filepath = BASE_DIR + '/examples/files/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        #mime_type = "application/zip"
        print(mime_type)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        return render(request,'index.html')

def enczip(filename='',pw='',pin=''):
    print("f2: "+filename, pw, pin)
    if filename !='':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        basename=filename.split('.')[0]
        #filepath = BASE_DIR + '/examples/files/' + basename+'-tfa.zip'
        filepath = BASE_DIR + '/examples/files/' + filename
        rc = subprocess.call(['7z', 'a', '-p'+pw, '-y', basename+'.zip', filename], cwd=BASE_DIR+'/examples/files/')
        rc = subprocess.call(['7z', 'a', '-p'+pin, '-y', basename+'-tfa.zip', basename+'.zip'], cwd=BASE_DIR+'/examples/files/')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
class CredsView(BSModalFormView):
    print("credsview")
    form_class = CredsInputForm
    template_name = 'examples/creds.html'
    success_message = 'Success: We will encrypt you file.'
    def get_filename(self):
        self.fn = self.kwargs['filename']
        return self.fn
    def form_valid(self,form):
        pw=form.cleaned_data['password']
        pin=form.cleaned_data['pin']
        fn=self.get_filename()
        enczip(fn,pw,pin)
        encfn=fn.split('.')[0]+'-tfa.zip'
        print(':'.join([pw,pin,fn]))
        self.success_url = '/download/'+encfn
        #return super(CredsView, self).form_valid(form)
        return redirect('/download/'+encfn)



class Index(generic.ListView):
    template_name = 'index.html'
