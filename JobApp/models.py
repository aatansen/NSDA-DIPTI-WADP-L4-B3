from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_user_model(AbstractUser):
    Display_name=models.CharField(max_length=100,null=True)
    USER=[
        ('recruiter','Job Recruiter'),
        ('seeker','Job Seeker'),
    ]
    User_Type=models.CharField(choices=USER,max_length=100,null=True)
    def __str__(self):
        return self.username

class Recruiter_model(models.Model):
    recruiter_user=models.OneToOneField(Custom_user_model,on_delete=models.CASCADE,related_name='recruiter_model',null=True)
    Company_logo=models.ImageField(upload_to='media/Company_logo')
    Company_name=models.CharField(max_length=100,null=True)
    Company_location=models.CharField(max_length=100,null=True)


class Seeker_model(models.Model):
    seeker_user=models.OneToOneField(Custom_user_model,on_delete=models.CASCADE,related_name='contactinfomodel',null=True)
    Skills=models.CharField(max_length=100,null=True)
    Resume_file=models.FileField(upload_to='media/Resume_file')

class Job_model(models.Model):
    created_by=models.ForeignKey(Custom_user_model,on_delete=models.CASCADE,related_name='addinfomodel',null=True)
    Job_title=models.CharField(max_length=100,null=True)
    Number_of_openings=models.IntegerField(null=True)
    Category=models.CharField(max_length=100,null=True)
    Job_description=models.TextField(null=True)
    Skills=models.CharField(max_length=100,null=True)

class Job_apply_model(models.Model):
    Applicant=models.ForeignKey(Custom_user_model,on_delete=models.CASCADE,null=True)
    Applied_Job=models.ForeignKey(Job_model,on_delete=models.CASCADE,null=True)
    Resume=models.FileField(upload_to='media/Resume',null=True)
    Skills=models.CharField(max_length=100,null=True)
    Status=models.CharField(default="Pending",max_length=100,null=True)