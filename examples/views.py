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


def download(request,filename='',pw='',pin=''):
    print("f2: "+filename, pw, pin)
    if filename !='':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        basename=filename.split('.')[0]
        filepath = BASE_DIR + '/examples/files/' + basename+'-tfa.zip'
        subprocess.call(['touch', 'examples/files/testme'])
        rc = subprocess.call(['7z', 'a', '-p'+pw, '-y', basename+'.zip', filename], cwd=BASE_DIR+'/examples/files/')
        rc = subprocess.call(['7z', 'a', '-p'+pin, '-y', basename+'-tfa.zip', basenaem+'.zip'], cwd=BASE_DIR+'/examples/files/')
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % basename+'-tfa.zip'
        # Return the response value
        return response
    else:
        return render(request,'index.html')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CredsView(BSModalFormView):
    print("credsview")
    #form_class = CredentialPromptForm
    form_class = CredsInputForm
    template_name = 'examples/creds.html'
    success_message = 'Success: We will encrypt you file.'
    #slug = None
    def get_filename(self):
        fn = self.kwargs['filename']
        return fn
    def form_valid(self,form):
        pw=form.cleaned_data['password']
        pin=form.cleaned_data['pin']
        filename=self.get_filename()
        print(':'.join([pw,pin,filename]))
        self.success_url = reverse_lazy('examples:download', kwargs={'pw':pw,'pin':pin,'filename':filename})
        return super(CredsView, self).form_valid(form)
    #success_url = reverse_lazy('examples:download')
    #success_url = reverse_lazy('examples:download')



class Index(generic.ListView):
    template_name = 'index.html'
