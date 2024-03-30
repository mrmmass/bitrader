from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_template_path

# Create your views here.

def home(request):
    template = get_template_path(request, 'home.html')
    return render(request, template)

@login_required
def main_account(request):
    template = get_template_path(request, 'index.html')
    return render(request, template)
@login_required
def html_templates(request , path):
    template = get_template_path(request, path)
    return render(request, template)