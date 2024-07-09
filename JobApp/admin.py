from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Custom_user_model)
admin.site.register(Recruiter_model)
admin.site.register(Seeker_model)
admin.site.register(Job_model)
admin.site.register(Job_apply_model)