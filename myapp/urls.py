from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',signupform,name='signupform'),
    path('doctor_dashboard/',doctor_dashboard,name='doctor_dashboard'),
    path('patient_dashboard/',patient_dashboard,name='patient_dashboard'),
    path('loginform/',loginform,name='loginform'),
    path('blog_form/',blog_form,name='blog_form'),
    path('blog_detail/<int:id>/',blog_detail,name='blog_detail'),
    path('blog_list/',blog_list,name='blog_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
