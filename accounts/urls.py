from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', login, {'template_name': 'accounts/login.html'}),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^pages/$', views.pages, name="pages"),
    url(r'^upload/$', views.model_upload_form, name="upload")
]