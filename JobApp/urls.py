from django.urls import path
from .views import *

urlpatterns=[
    path('signup/',signup,name='signup'),
    path('',signin,name='signin'),
    path('dashboard/',dashboard,name='dashboard'),
    path('signout/',signout,name='signout'),
    path('addjob/',addjob,name='addjob'),
    path('joblist/',joblist,name='joblist'),
    path('deletejob/<str:jobid>',deletejob,name='deletejob'),
    path('editjob/<str:jobid>',editjob,name='editjob'),
    path('applyjob/<str:jobid>',applyjob,name='applyjob'),
    path('baseprofile/',baseprofile,name='baseprofile'),
    path('basicinfo/',basicinfo,name='basicinfo'),
    path('seekerotherinfo/',seekerotherinfo,name='seekerotherinfo'),
    path('recruiterotherinfo/',recruiterotherinfo,name='recruiterotherinfo'),
    path('appliedjob/',appliedjob,name='appliedjob'),
    path('postedjob/',postedjob,name='postedjob'),
    path('applicants/<str:jobid>',applicants,name='applicants'),
    path('callforinterview/<str:jobid>',callforinterview,name='callforinterview'),
    path('rejected/<str:jobid>',rejected,name='rejected'),
    path('editprofile/',editprofile,name='editprofile'),
    path('jobsearch/',jobsearch,name='jobsearch'),
    path('skillmatched/',skillmatched,name='skillmatched'),
    path('change_password/',change_password,name='change_password'),
]