import os
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from app.views import SubmitFormView,homeView,analyze

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeView, name="home"),
    path('analyze/',analyze, name="analyze"),
    path('submitForm/',SubmitFormView.as_view()),
    url(r'^fp/', include('django_drf_filepond.urls')),
    url(r'^demo/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR,'templates')}),

]
