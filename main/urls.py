from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main_account, name='main_account'),
    path('main/<path:path>', views.html_templates, name='html_templates'),
    path(r'_service-worker.js', (TemplateView.as_view(template_name="_service-worker.js", content_type='application/javascript', )), name='_service-worker.js'),
]
