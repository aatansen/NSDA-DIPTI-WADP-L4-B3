from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

# Create your views here.
def signup(request):
    if request.method=="POST":
        form=Custom_user_form(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            if user.User_Type == 'recruiter':
                Recruiter_model.objects.create(
                    recruiter_user=user
                )
            elif user.User_Type == 'seeker':
                Seeker_model.objects.create(
                    seeker_user=user
                )
            return redirect('signin')
    else:
        form=Custom_user_form()
    context={
        'form':form
    }
    return render(request,'common/signup.html',context)

def signin(request):
    if request.method=="POST":
        form=Auth_form(request,request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        form=Auth_form()
    context={
        'form':form
    }
    return render(request,'common/signin.html',context)


def dashboard(request):
    return render(request,'common/dashboard.html')

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def addjob(request):
    current_user=request.user
    if request.method=="POST":
        form=Job_form(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.created_by=current_user
            user.save()
            return redirect('joblist')
    else:
        form=Job_form()
    context={
        'form':form
    }
    return render(request,'recruiter/addjob.html',context)

@login_required
def editjob(request,jobid):
    job=get_object_or_404(Job_model,id=jobid)
    if request.method=="POST":
        form=Job_form(request.POST,instance=job)
        if form.is_valid():
            form.save()
            return redirect('joblist')
    else:
        form=Job_form(instance=job)
    context={
        'form':form
    }
    return render(request,'recruiter/editjob.html',context)

def joblist(request):
    jobs=Job_model.objects.all()
    if request.user.is_authenticated:
        joblist=[]
        for i in jobs:
            already_applied=Job_apply_model.objects.filter(Applicant=request.user,Applied_Job=i).exists()
            joblist.append(
                (i,already_applied),
            )

    elif request.user.is_anonymous:
        joblist=Job_model.objects.all()

    return render(request,'common/joblist.html',{'joblist':joblist})

@login_required
def deletejob(request,jobid):
    job=get_object_or_404(Job_model,id=jobid)
    job.delete()
    return redirect('joblist')

@login_required
def applyjob(request,jobid):
    current_user=request.user
    job=get_object_or_404(Job_model,id=jobid)
    if request.method=="POST":
        form=Job_apply_form(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.Applied_Job=job
            user.Applicant=current_user
            user.save()
            return redirect('joblist')
    else:
        form=Job_apply_form()
    return render(request,'seeker/applyjob.html',{'form':form})

@login_required
def baseprofile(request):
    return render(request,'profile/baseprofile.html')

@login_required
def basicinfo(request):
    return render(request,'profile/basicinfo.html')

@login_required
def seekerotherinfo(request):
    user_info=Seeker_model.objects.get(seeker_user=request.user)
    return render(request,'profile/seekerotherinfo.html',{'user_info':user_info})

@login_required
def recruiterotherinfo(request):
    user_info=Recruiter_model.objects.get(recruiter_user=request.user)
    context={
        'user_info':user_info
    }
    return render(request,'profile/recruiterotherinfo.html',context)


@login_required
def appliedjob(request):
    current_user=request.user
    applied_job=Job_apply_model.objects.filter(Applicant=current_user)
    return render(request,'seeker/appliedjob.html',{'applied_job':applied_job})

@login_required
def postedjob(request):
    current_user=request.user
    jobs=Job_model.objects.filter(created_by=current_user)
    return render(request,'recruiter/postedjob.html',{'jobs':jobs})

@login_required
def applicants(request,jobid):
    job=Job_model.objects.get(id=jobid)
    applicantdata=Job_apply_model.objects.filter(Applied_Job=job)
    context={
        'applicantdata':applicantdata,
        'job':job
    }
    return render(request,'recruiter/applicants.html',context)

@login_required
def callforinterview(request,jobid):
    applicant=Job_apply_model.objects.get(id=jobid)
    applicant.Status="Called for Interview"
    applicant.save()
    return redirect('postedjob')

@login_required
def rejected(request,jobid):
    applicant=Job_apply_model.objects.get(id=jobid)
    applicant.Status="Rejected"
    applicant.save()
    return redirect('postedjob')

@login_required
def editprofile(request):
    current_user=request.user
    if current_user.User_Type=='recruiter':
        recruiter=Recruiter_model.objects.get(recruiter_user=current_user)
    else:
        seeker=Seeker_model.objects.get(seeker_user=current_user)
    if request.method=='POST':
        form1=Edit_basic_form(request.POST,instance=current_user)
        if form1.is_valid():
            form1.save()
        if current_user.User_Type=='recruiter':
            form2=Edit_recruiter_form(request.POST,request.FILES,instance=recruiter)
            if form2.is_valid():
                form2.save()
        elif current_user.User_Type=='seeker':
            form3=Edit_seeker_form(request.POST,request.FILES,instance=seeker)
            if form3.is_valid():
                form3.save()
        return redirect('baseprofile')
    else:
        form1=Edit_basic_form(instance=current_user)
        if current_user.User_Type=='recruiter':
            form2=Edit_recruiter_form(instance=recruiter)
            context={
                'form1':form1,
                'form2':form2,
            }
        elif current_user.User_Type=='seeker':
            form3=Edit_seeker_form(instance=seeker)
            context={
                'form1':form1,
                'form3':form3,
            }
    return render(request,'common/editprofile.html',context)

@login_required
def jobsearch(request):
    search=request.GET.get('search')
    jobs = Job_model.objects.filter(
        Q(Job_title__icontains=search)
        )
    job_filtered=[]
    for i in jobs:
        already_applied=Job_apply_model.objects.filter(Applicant=request.user,Applied_Job=i).exists()
        job_filtered.append(
            (i,already_applied),
        )
    jobDict={
        'job_filtered':job_filtered
    }
    return render(request,'common/jobsearch.html',jobDict)

@login_required
def skillmatched(request):
    search=request.GET.get('search')
    jobs = Job_model.objects.filter(
        Q(Skills__icontains=search)
        )
    job_filtered=[]
    for i in jobs:
        already_applied=Job_apply_model.objects.filter(Applicant=request.user,Applied_Job=i).exists()
        job_filtered.append(
            (i,already_applied),
        )
    jobDict={
        'job_filtered':job_filtered
    }
    return render(request,'common/skillmatched.html',jobDict)

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        new_confirm_password=request.POST.get('new_confirm_password')
        
        checking=check_password(old_password,request.user.password)
        if checking:
            if new_password==new_confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request,request.user)
                return redirect('dashboard')
    return render(request,'profile/change-password.html')