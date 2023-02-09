from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from base import models
# from .models import  User, DictionaryList, SpeechList, HskLevel, Lesson, Quiz, Result, ActivityLog, MockTest
# from .forms import MyUserCreationForm, UserForm, DictionaryListForm, LessonForm
from base import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from difflib import SequenceMatcher
from django.core.paginator import Paginator
import random
import json

# Create your views here.


@login_required(login_url='anonymous')
def PasswordReset(request):
    if request.method == 'POST':
        user = request.user
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        
        formErrors = 0
        s_1 = user.username
        s_2 = newpassword
        ratio = SequenceMatcher(a=s_1,b=s_2).ratio()
        s_3 = user.email
        ratio2 = SequenceMatcher(a=s_3,b=s_2).ratio()

        if ratio >= 0.6 and ratio <= 1 or ratio2 >= 0.6 and ratio2 <= 1:
            messages.error(request, 'Password can’t be too similar to your other personal information.')
            formErrors += 1
        if newpassword != confirmpassword:
            messages.error(request, 'Password do not match')
            formErrors += 1
        if str(newpassword).isalpha() or str(newpassword).isnumeric():
            messages.error(request, 'Password must be composed of alphanumeric characters')
            formErrors += 1
        if len(newpassword) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            formErrors += 1
        user = authenticate(request, username = user.username, password= oldpassword)
        if user is None: 
            messages.warning(request, 'old password is incorrect')
            formErrors += 1
        if formErrors == 0:
            if user is not None:
                user.password = make_password(newpassword)
                user.save()
                login(request, user)
                messages.success(request, 'Password changed.')
                models.ActivityLog.objects.create(
                    user = user,
                    action = f"Password changed",
                    )
                return redirect('password-reset')
            else:
                return redirect('password-reset')
        else:
            return redirect('password-reset')
    ctx={}
    return render(request, 'change_password.html',ctx)

def PleaseLoginToAccessThisPage(request):
    messages.info(request, 'Please log in to access this page')
    return redirect('login')

@login_required(login_url='anonymous')
def LogoutUser(request):
    
    messages.info(request, 'You have been logged out')
    models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"Logged out",
            )
    logout(request)        
    return redirect('login')


def RegisterPage(request):
    form = forms.MyUserCreationForm()
    formErrors = 0
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('admin-dashboard')
    if request.method == 'POST':
        s_1 = request.POST.get('username')
        s_2 = request.POST.get('password1')
        ratio = SequenceMatcher(a=s_1,b=s_2).ratio()
        s_3 = request.POST.get('email')
        ratio2 = SequenceMatcher(a=s_3,b=s_2).ratio()

        if ratio >= 0.6 and ratio <= 1 or ratio2 >= 0.6 and ratio2 <= 1:
            messages.error(request, 'Password can’t be too similar to your other personal information.')
            formErrors += 1
        
        if request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request, 'Password do not matched!')
            formErrors += 1
        if len(request.POST.get('password1')) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            formErrors += 1
        if str(request.POST.get('password1')).isnumeric() or str(request.POST.get('password1')).isalpha():
            messages.error(request, 'Password must be composed of alphanumeric characters')
            formErrors += 1
        if models.Faculty.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, f"{request.POST.get('username')} already exists!")
            formErrors += 1
        if models.Faculty.objects.filter(email=request.POST.get('email')).exists():
            messages.error(request, f"{request.POST.get('email')} already exists!")
            formErrors += 1
        if models.Faculty.objects.filter(emp_no=request.POST.get('emp_no')).exists():
            messages.error(request, f"{request.POST.get('emp_no')} already exists!")
            formErrors += 1
        if models.Faculty.objects.filter(contact_no=request.POST.get('contact_no')).exists():
            messages.error(request, f"{request.POST.get('contact_no')} already exists!")
            formErrors += 1
        if formErrors == 0:
            form = forms.MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                
                user.username = user.username.lower()
                user.first_name = user.first_name.title()
                user.last_name = user.last_name.title()
                user.role = 1
                
                user.save()

                models.ActivityLog.objects.create(
                user = user,
                action = f"New user is registered - {user.username}",
                )
                login(request, user)
                messages.success(request, f'You are logged in as {user.username}')
                return redirect('faculty-research')
            else:
                for field, errors in form.errors.items():
                    messages.error(request, '{}'.format(''.join(errors)))
                # return redirect('register')
        else:
            return redirect('register')
    ctx={
        'form': form,
    }
    return render(request, 'register.html', ctx)

def LoginPage(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('admin-dashboard')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        formErrors = 0

        if "@" in username:
            try:
                user = models.Faculty.objects.get(email = username)
                username = user.username 
            except:
                formErrors += 1
                messages.error(request, f'{username} does not exist')
                return redirect('login')
        else:
            try:
                user = models.Faculty.objects.get(username = username)
            except:
                formErrors += 1
                messages.error(request, f'{username} does not exist')
                return redirect('login')
        
        if formErrors == 0:
            user = authenticate(request, username = username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, f'You are logged in as {username}')
                    models.ActivityLog.objects.create(
                    user = user,
                    action = f"Logged In",
                    )
                    return redirect('admin-dashboard')
                else:
                    login(request, user)
                    messages.success(request, f'You are logged in as {username}')
                    models.ActivityLog.objects.create(
                    user = user,
                    action = f"Logged In",
                    )
                    return redirect('faculty-research')
            else:
                messages.warning(request, 'Invalid credentials!')
                return redirect('login')
    ctx = {}
    return render(request, 'login.html', ctx)
@login_required(login_url='anonymous')
def AdminDashboard(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.info(request, 'You are already logged in')
        return redirect('logout')
    ctx = {
        "active" : "admin_dashboard",
    }
    
    return render(request, 'admin_dashboard.html', ctx)

@login_required(login_url='anonymous')
def AdminFaculty(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
            Q(role = 1),
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search), 
    
        ).order_by('created_at')

  
    p = Paginator(faculty, 6)
    page = request.GET.get('page')
    faculty = p.get_page(page)
    
    ctx = {
        "faculty" : faculty,
        "active" : "admin_faculty",
        'search' : search,
        'page' : page,
    }
    
    return render(request, 'admin_faculty.html', ctx)

@login_required(login_url='anonymous')
def AdminDepartmentHead(request):
    
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
            Q(role = 2),
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search), 
    
        ).order_by('created_at')

  
    p = Paginator(faculty, 6)
    page = request.GET.get('page')
    faculty = p.get_page(page)
    
    ctx = {
        "faculty" : faculty,
        "active" : "admin_faculty",
        'search' : search,
        'page' : page,
    }
    
    
    return render(request, 'admin_department.html', ctx)


@login_required(login_url='anonymous')
def AdminActivityLog(request):
    
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    activity_logs = models.ActivityLog.objects.filter(
        Q(user__username__icontains = search) |
        Q(created_at__icontains = search) 
        ).order_by('created_at')
    p = Paginator(activity_logs, 6)
    page = request.GET.get('page', 1)
    activity_logs = p.get_page(page)
    
    ctx = {
        "active" : "admin_activitylogs",
        "table_data" : activity_logs,
        'search' : search,
        'page' : page,
    }
    
    
    return render(request, 'admin_activitylogs.html', ctx)

@login_required(login_url='anonymous')    
def AdminDeleteActivityLog(request, pk):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    activitylog = models.ActivityLog.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{activitylog.action} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted activity log",
            )
        activitylog.delete()
        return redirect('admin-activitylog')
    
    ctx = {
        "obj": activitylog,
        "active" : "admin_activitylog",
        "label" : "ActivityLog",
        "link" : redirect('admin-activitylog').url,
    }
    return render(request, 'all_delete.html', ctx)


@login_required(login_url='anonymous')
def AdminResearchCoordinator(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
            Q(role = 3),
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search), 
    
        ).order_by('created_at')

  
    p = Paginator(faculty, 6)
    page = request.GET.get('page')
    faculty = p.get_page(page)
    
    ctx = {
        
        "faculty" : faculty,
        "active" : "admin_faculty",
        'search' : search,
        'page' : page,
    }
    
    
    return render(request, 'admin_research.html', ctx)

@login_required(login_url='anonymous')
def AdminExtensionCoordinator(request):
    
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
            Q(role = 4),
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search), 
    
        ).order_by('created_at')

  
    p = Paginator(faculty, 6)
    page = request.GET.get('page')
    faculty = p.get_page(page)
    
    ctx = {
        "faculty" : faculty,
        "active" : "admin_faculty",
        'search' : search,
        'page' : page,
    }
    
    
    return render(request, 'admin_extension.html', ctx)

@login_required(login_url='anonymous')
def EditProfile(request):
    user = request.user
    form = forms.UserForm(instance=user)
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
           
                
            user.save()
            messages.success(request, "Account updated!")
            models.ActivityLog.objects.create(
                user = request.user,
                action = "Update account information",
            )
            return redirect('edit-profile')
        else :
            for field, errors in form.errors.items():
                messages.error(request, '{}'.format(''.join(errors)))
            return redirect('edit-profile')
    link = ''
    if request.user.is_authenticated and request.user.is_staff:
        link = redirect('admin-dashboard').url
    else :
        link = redirect('faculty-research').url
    
    ctx={
          'link': link,
          'form': form,
          'page' : 'authenticated'
    }
    
    return render(request, 'edit_profile.html', ctx)

@login_required(login_url='anonymous')
def AdminEditProfile(request, pk):
    user = models.Faculty.objects.get(id=pk)
    form = forms.UserForm(instance=user)
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated!")
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} updated account of {user.username}",
            )
            return redirect('admin-edit-profile', pk=user.id)
        else :
            for field, errors in form.errors.items():
                messages.error(request, '{}'.format(''.join(errors)))
            return redirect('admin-edit-profile', pk=user.id)
    context = {
        'form': form,
         'user' : user,
         'link' : redirect('admin-faculty').url
    }
    return render(request, 'edit_profile.html', context)

@login_required(login_url='anonymous')
def ChangeRole(request, pk, num, department):
    if request.method == 'GET':
        if request.user.is_authenticated and not request.user.is_staff:
            return JsonResponse({'success': False})
        faculty = models.Faculty.objects.get(id=pk)
        dept = models.Department.objects.get(title=department)
    
        if len(models.Faculty.objects.filter(role = 2, department=dept.id)) != 0 and int(num) == 2:
            messages.warning(request, f'Only one department head is allowed per department.')
            return JsonResponse({'success': False})
  
              
        
        
        faculty.role = int(num)
        
        faculty.save()
        role_list = ['Faculty', 'Department Head', 'Research Coordinator', 'Extension Coordinator']
        role_name = role_list[int(num)-1]
        
        
        messages.info(request, f'{faculty.first_name} {faculty.last_name} changed role to {role_name}')
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f'{faculty.first_name} {faculty.last_name} changed role to {role_name}'
            )
        return JsonResponse({"success": True})
    
    
@login_required(login_url='anonymous')    
def AdminDeleteFaculty(request, pk):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    faculty = models.Faculty.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{faculty.username} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted the account of {faculty.username}",
            )
        faculty.delete()
        return redirect('admin-faculty')
    
    ctx = {
        "obj": faculty,
        "active" : "admin_faculty",
        "label" : "Faculty",
        "link" : redirect('admin-faculty').url,
    }
    return render(request, 'all_delete.html', ctx)

# SUBJECT CRUD 

@login_required(login_url='anonymous')    
def AdminSubject(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    subjects = models.Subject.objects.filter(
        Q(units__icontains = search) |
        Q(code__icontains = search) |
        Q(title__icontains = search) 
        )
    p = Paginator(subjects, 6)
    page = request.GET.get('page')
    subjects = p.get_page(page)
    
    ctx = {
        'table_data': subjects,
        'search' : search,
        "active" : "admin_subject",
        'page' : page,
    }
    return render(request, 'admin_subject.html', ctx)


@login_required(login_url='anonymous')    
def AdminAddSubject(request):
    form = forms.SubjectForm()
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST)
        if form.is_valid():
            print(models.Subject.objects.filter(title=request.POST.get('title')).exists())
            if not models.Subject.objects.filter(title=request.POST.get('title')).exists() \
                or not models.Subject.objects.filter(code=request.POST.get('code')).exists():
                subject = form.save(commit=False)
                subject.title = subject.title.title()
                subject.save()
                messages.success(request, 'Subject added')
                models.ActivityLog.objects.create(
                        user = request.user,
                        action = f"{request.user.username} added new subject",
                )
                return redirect('admin-subject')
            else:
                messages.error(request, 'Subject info already existing')
                return redirect('admin-add-subject')
        else : 
            messages.error(request, 'Subject info already existing')
            return redirect('admin-add-subject')
    ctx = {
        "active" : "admin_subject",
        "form" : form,
        "label" : "add",
        'link': redirect('admin-subject').url
    }
    return render(request, 'subject_edit_add.html', ctx)

    
    
@login_required(login_url='anonymous')
def AdminEditSubject(request, pk):
    subject_list = models.Subject.objects.get(id=pk)
    form = forms.SubjectForm(instance=subject_list)
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST, instance=subject_list)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a subject",
            )
            return redirect('admin-edit-subject', pk=subject_list.id)
    ctx = {
        "active" : "admin_subject",
        'form' : form,
        'label' : 'update',
        'link': redirect('admin-subject').url
    }
    return render(request, 'subject_edit_add.html', ctx)


@login_required(login_url='anonymous')    
def AdminDeleteSubject(request, pk):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    subject = models.Subject.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{subject.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted the subject of {subject.title}",
            )
        subject.delete()
        return redirect('admin-subject')
    
    ctx = {
        "obj": subject,
        "active" : "admin_subject",
        "label" : "Subject",
        "link" : redirect('admin-subject').url,
    }
    return render(request, 'all_delete.html', ctx)
# RESEARCH CRUD

@login_required(login_url='anonymous')    
def AdminResearches(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    researches = models.Research.objects.filter(
        Q(title__icontains = search) |
        Q(detail__icontains = search) |
        Q(status__status__icontains = search) 
        )
    p = Paginator(researches, 6)
    page = request.GET.get('page')
    researches = p.get_page(page)
    
    
    
    ctx = {
        "table_data" : researches,
        "active" : "admin_researches",
        'page' : page,
        'search' : search,
    }
    return render(request, 'all_research.html', ctx)

@login_required(login_url='anonymous')    
def AdminAddResearch(request):
    form = forms.ResearchFormWithUser()
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ResearchFormWithUser(request.POST, request.FILES)
        if form.is_valid():
            # print(request.FILES['file'].name)
            research = form.save(commit=False)
            
            research.filename = request.FILES['file'].name
            research.title = research.title.title()
            research.save()
            messages.success(request, 'Research added')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added new research",
            )
            return redirect('admin-researches')
            
    ctx = {
        "active" : "admin_researches",
        "form" : form,
        "label" : "add",
        'link' : redirect('admin-researches').url
    }
    return render(request, 'research_edit_add.html', ctx)


@login_required(login_url='anonymous')
def AdminEditResearch(request, pk):
    research = models.Research.objects.get(id=pk)
    form = forms.ResearchFormWithUser(instance=research)
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ResearchFormWithUser(request.POST, instance=research)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a research",
            )
            return redirect('admin-edit-research', pk=research.id)
    ctx = {
        "active" : "admin_researches",
        'form' : form,
        'label' : 'update',
        'link' : redirect('admin-researches').url
    }
    return render(request, 'research_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def AdminDeleteResearch(request, pk):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    research = models.Research.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{research.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted the research of {research.title}",
            )
        research.delete()
        return redirect('admin_researches')
    
    ctx = {
        "obj": research,
        "active" : "admin_researches",
        "label" : "Research",
        "link" : redirect('admin-researches').url,
    }
    return render(request, 'all_delete.html', ctx)


# EXTENSION CRUD
@login_required(login_url='anonymous')    
def AdminExtensionService(request):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')

    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    extension = models.ExtensionService.objects.filter(
        Q(title__icontains = search) |
        Q(detail__icontains = search) |
        Q(project__project_detail__icontains = search) 
        ).distinct().order_by('created_at')
    p = Paginator(extension, 6)
    page = request.GET.get('page')
    extension = p.get_page(page)
    
    ctx = {
        'table_data': extension,
        'search' : search,
        "active" : "admin_extension_service",
        'page' : page,
    }
    return render(request, 'admin_extension_service.html', ctx)



@login_required(login_url='anonymous')    
def AdminAddExtensionService(request):
    form = forms.ExtensionServiceForm()
    label = "Add"
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ExtensionServiceForm(request.POST)
        if form.is_valid():
            extension = form.save(commit=False)
            extension.title = extension.title.title()
            extension.save()
            messages.success(request, 'Extension Service added')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added new extension service",
            )
            return redirect('admin-edit-extension-service', pk=extension.id)
            
    ctx = {
        "active" : "admin_extension_service",
        "form" : form,
        "label" : "add",
        "link" : redirect('admin-extension-service').url,
    }
    return render(request, 'extension_edit_add.html', ctx)

    
    
@login_required(login_url='anonymous')
def AdminEditExtensionService(request, pk):
    extension = models.ExtensionService.objects.get(id=pk)
    form = forms.ExtensionServiceForm(instance=extension)
    project_form = forms.ProjectForm()
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST' and request.POST.get('title') and request.POST.get('detail'):
        form = forms.ExtensionServiceForm(request.POST, instance=extension)
        if form.is_valid():
            print('extension')
            form.save()
            messages.success(request, 'Subject updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a subject",
            )
            return redirect('admin-edit-extension-service', pk=extension.id)
    if request.method == 'POST' and request.POST.get('project_detail'):
        project_form = forms.ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.extension = extension
            project.save()
            
            messages.success(request, 'Project Added to Extension Service')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added project to {extension.title}",
            )
            return redirect('admin-edit-extension-service', pk=extension.id)
            
        
    ctx = {
        "active" : "admin_extension_service",
        'form' : form,
        'project_form': project_form,
        'label' : 'update',
        'extension' : extension,
        "link" : redirect('admin-extension-service').url,
    }
    return render(request, 'extension_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def AdminDeleteExtensionService(request, pk):
    if request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    extension = models.ExtensionService.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{extension.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted extension {extension.title}",
            )
        extension.delete()
        return redirect('admin-extension-service')
    ctx = {
        "obj": extension,
        "active" : "admin-extension-service",
        "label" : "Extension Service",
        "link" : redirect('admin-extension-service').url,
    }
    return render(request, 'all_delete.html', ctx)


# PROJECT

@login_required(login_url='anonymous')
def DeleteProject(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and not request.user.is_staff:
            return JsonResponse({'success': False})
     
        project = models.Project.objects.get(id=pk)
        
        
        
        messages.info(request, f'project deleted from {project.extension.title}')
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f'{request.user.username} delete a project from {project.extension.title}'
            )
        
        project.delete()
        return JsonResponse({"success": True})



# FACULTY RESEARCH END

@login_required(login_url='anonymous')
def FacultyResearch(request):
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    researches = models.Research.objects.filter(
        Q(title__icontains = search) |
        Q(detail__icontains = search) |
        Q(status__status__icontains = search) 
        ).order_by('created_at')
    status = models.ResearchStatus.objects.all()
    
    p = Paginator(researches, 6)
    page = request.GET.get('page')
    researches = p.get_page(page)
    
    research_all = models.Research.objects.all()
    print(research_all)
    ctx={
        'table_data' : researches,
        'search':search,
        'page' : page,
        'active' : 'faculty_research',
        'status':status,
        
        'research_all': research_all,
    }
    return render(request, 'faculty_research.html',ctx)


@login_required(login_url='anonymous')    
def FacultyAddResearch(request):
    form = forms.ResearchFormNoUser()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ResearchFormNoUser(request.POST, request.FILES)
        if form.is_valid():
            # print(request.FILES['file'].name)
            research = form.save(commit=False)
            
            research.filename = request.FILES['file'].name
            research.user = request.user
            research.title = research.title.title()
            research.save()
            messages.success(request, 'Research added')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added new research",
            )
            return redirect('faculty-research')
            
    ctx = {
        "active" : "faculty_research",
        "form" : form,
        "label" : "add",
        'link' : redirect('faculty-research').url
    }
    return render(request, 'research_edit_add.html', ctx)


@login_required(login_url='anonymous')    
def FacultyMyResearch(request):
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    researches = models.Research.objects.filter(
        Q(user = request.user.id),
        Q(title__icontains = search) |
        Q(detail__icontains = search) |
        Q(status__status__icontains = search) 
        )
    p = Paginator(researches, 6)
    page = request.GET.get('page')
    researches = p.get_page(page)
    
    
 
    ctx = {
        "table_data" : researches,
        "active" : "faculty_research",
        'page' : page,
        'search' : search,
    }
    return render(request, 'all_my_research.html', ctx)


@login_required(login_url='anonymous')
def FacultyEditResearch(request, pk):
    research = models.Research.objects.get(id=pk)
    form = forms.ResearchFormNoUser(instance=research)
    if request.user.is_authenticated and  request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ResearchFormNoUser(request.POST, instance=research)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a research",
            )
            return redirect('faculty-edit-research', pk=research.id)
    ctx = {
        "active" : "faculty_research",
        'form' : form,
        'label' : 'update',
        "link" : redirect('faculty-my-research').url,
    }
    return render(request, 'research_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def FacultyDeleteResearch(request, pk):
    if request.user.is_authenticated and  request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    research = models.Research.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{research.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted the research of {research.title}",
            )
        research.delete()
        return redirect('faculty-research')

    
    ctx = {
        "obj": research,
        "active" : "faculty_research",
        "label" : "Research",
        "link" : redirect('faculty-research').url,
    }
    return render(request, 'all_delete.html', ctx)

def FacultyResearchDetail(request, pk):
    
    research = models.Research.objects.get(id=pk)
    
    ctx={'research': research,
         "active" : "faculty_research",}
    
    return render(request, 'faculty_research_detail.html', ctx)


# FACULTY SUBJECT END -----------------------------------

@login_required(login_url='anonymous')    
def FacultySubject(request):
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
   
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    subjects = models.FacultySubject.objects.filter(
        Q(user = request.user.id),
        Q(subject__units__icontains = search) |
        Q(subject__code__icontains = search) |
        Q(subject__title__icontains = search) 
        )
    p = Paginator(subjects, 6)
    page = request.GET.get('page')
    subjects = p.get_page(page)
    
    ctx = {
        'table_data': subjects,
        'search' : search,
        "active" : "faculty_subject",
        'page' : page,
    }
    return render(request, 'faculty_subject.html', ctx)


@login_required(login_url='anonymous')    
def FacultyAddPresetSubject(request):
    form = forms.FacultySubjectForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.FacultySubjectForm(request.POST)
        print(form, request.POST)
        if form.is_valid():
            if models.FacultySubject.objects.filter(user=request.user.id, subject=request.POST.get('subject')).exists():
                messages.warning(request, 'Cannot add the same subject to your list')
                return redirect('faculty-add-preset-subject')
            
            faculty_subject = form.save(commit=False)
            faculty_subject.user = request.user
            faculty_subject.save()
            messages.success(request, 'Subject added to your list')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added preset subject",
            )
            return redirect('faculty-subject')
          
    ctx = {
        "active" : "faculty_subject",
        "form" : form,
        "label" : "add",
        "link" : redirect('faculty-subject').url,
    }
    return render(request, 'subject_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def FacultyAddOwnSubject(request):
    form = forms.SubjectForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            if not models.Subject.objects.filter(title=request.POST.get('title')).exists() \
                or not models.Subject.objects.filter(code=request.POST.get('code')).exists():
                subject = form.save(commit=False)
                subject.title = subject.title.title()
                subject.is_preset = False
                subject.save()
                
                faculty_subject = models.FacultySubject.objects.create(
                    user = request.user,
                    subject = subject,
                )
                
                messages.success(request, 'Subject added')
                models.ActivityLog.objects.create(
                        user = request.user,
                        action = f"{request.user.username} added new subject",
                )
                return redirect('faculty-subject')
            else:
                messages.error(request, 'Subject info already existing')
                return redirect('faculty-add-subject')
        else : 
            messages.error(request, 'Subject info already existing')
            return redirect('faculty-add-subject')
            
    ctx = {
        "active" : "faculty_subject",
        "form" : form,
        "label" : "add",
       "link" : redirect('faculty-subject').url,
    }
    return render(request, 'subject_edit_add.html', ctx)

    
    
@login_required(login_url='anonymous')
def FacultyEditSubject(request, pk):
    subject_list = models.Subject.objects.get(id=pk)
    form = forms.SubjectForm(instance=subject_list)
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST, instance=subject_list)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a subject",
            )
            return redirect('faculty-edit-subject', pk=subject_list.id)
    ctx = {
        "active" : "faculty_subject",
        'form' : form,
        'label' : 'update',
        "link" : redirect('faculty-subject').url,
    }
    return render(request, 'subject_edit_add.html', ctx)


@login_required(login_url='anonymous')    
def FacultyDeleteSubject(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    subject = models.Subject.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{subject.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted the subject of {subject.title}",
            )
        subject.delete()
        return redirect('faculty-subject')
    
    ctx = {
        "obj": subject,
        "active" : "faculty_subject",
        "label" : "Subject",
        "link" : redirect('faculty-subject').url,
    }
    return render(request, 'all_delete.html', ctx)


# Faculty EXTENSION ||||||||||||||||||||||||||||||||||||||||||||||||||||||

@login_required(login_url='anonymous')    
def FacultyExtensionService(request):
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')

    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    extension = models.FacultyExtension.objects.filter(
        Q(user = request.user.id) ,
        Q(extension__title__icontains = search) |
        Q(extension__detail__icontains = search) |
        Q(extension__project__project_detail__icontains = search) 
        ).distinct().order_by('extension__created_at')
    p = Paginator(extension, 6)
    page = request.GET.get('page')
    extension = p.get_page(page)
    
    ctx = {
        'table_data': extension,
        'search' : search,
        "active" : "faculty_extension_service",
        'page' : page,
    }
    return render(request, 'faculty-extension-service.html', ctx)


@login_required(login_url='anonymous')    
def FacultyAddPresetExtensionService(request):
    form = forms.FacultyExtensionForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.FacultyExtensionForm(request.POST)
        if form.is_valid():
            if models.FacultyExtension.objects.filter(user=request.user.id, extension=request.POST.get('extension')).exists():
                messages.warning(request, 'Cannot add the same extension to your list')
                return redirect('faculty-add-preset-extension-service')
            
            faculty_extension = form.save(commit=False)
            faculty_extension.user = request.user
            faculty_extension.save()
            messages.success(request, 'Extension added to your list')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added preset extension",
            )
            return redirect('faculty-extension-service')
          
    ctx = {
        "active" : "faculty_extension_service",
        "form" : form,
        "label" : "add",
        "link" : redirect('faculty-extension-service').url,
    }
    return render(request, 'extension_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def FacultyAddOwnExtensionService(request):
    form = forms.ExtensionServiceForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.ExtensionServiceForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            if models.ExtensionService.objects.filter(title=request.POST.get('title')):
                messages.warning(request, 'Extension info already exists')
                return redirect('faculty-add-preset-extension')
            extension = form.save(commit=False)
            extension.title = extension.title.title()
            extension.is_preset = False
            extension.save()
            
            faculty_extension = models.FacultyExtension.objects.create(
                user = request.user,
                extension = extension,
            )
            
            messages.success(request, 'Extension Service added')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added new extension service",
            )
            return redirect('faculty-edit-extension-service', pk=extension.id)
            
           
            
    ctx = {
        "active" : "faculty_extension_service",
        "form" : form,
        "label" : "add",
       "link" : redirect('faculty-extension-service').url,
    }
    return render(request, 'extension_edit_add.html', ctx)



@login_required(login_url='anonymous')
def FacultyEditExtensionService(request, pk):
    extension = models.ExtensionService.objects.get(id=pk)
    form = forms.ExtensionServiceForm(instance=extension)
    project_form = forms.ProjectForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST' and request.POST.get('title') and request.POST.get('detail'):
        form = forms.ExtensionServiceForm(request.POST, instance=extension)
        if form.is_valid():
            print('extension')
            form.save()
            messages.success(request, 'Subject updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited a subject",
            )
            return redirect('faculty-edit-extension-service', pk=extension.id)
    if request.method == 'POST' and request.POST.get('project_detail'):
        project_form = forms.ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.extension = extension
            project.save()
            
            messages.success(request, 'Project Added to Extension Service')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} added project to {extension.title}",
            )
            return redirect('faculty-edit-extension-service', pk=extension.id)
            
        
    ctx = {
        "active" : "faculty_extension_service",
        'form' : form,
        'project_form': project_form,
        'label' : 'update',
        'extension' : extension,
        "link" : redirect('faculty-extension-service').url,
    }
    return render(request, 'extension_edit_add.html', ctx)

@login_required(login_url='anonymous')    
def FacultyDeleteExtensionService(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    extension = models.ExtensionService.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{extension.title} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted extension {extension.title}",
            )
        extension.delete()
        return redirect(['faculty-extension-service'])
    ctx = {
        "obj": extension,
        "active" : "faculty_extension_service",
        "label" : "Extension Service",
        "link" : redirect('faculty-extension-service').url,
    }
    return render(request, 'all_delete.html', ctx)


# DEPARTMENTHEAD END

@login_required(login_url='anonymous')
def DepartmentHeadFaculty(request):
    if (request.user.is_authenticated and request.user.is_staff) or (request.user.is_authenticated and request.user.role in [3,4]):
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
        Q(department = request.user.department.id),
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search)| 
        Q(facultysubject__subject__title__icontains = search),
    
        ).distinct().order_by('created_at')

    subjects = models.Subject.objects.all()
    
    p = Paginator(faculty, 6)
    page = request.GET.get('page')
    faculty = p.get_page(page)
    
    ctx = {
        "faculty" : faculty,
        "active" : "manage_department",
        'search' : search,
        'page' : page,
        'subjects' : subjects
    }
    
    return render(request, 'department_head_faculty.html', ctx)


@login_required(login_url='anonymous')
def DepartmentHeadEditFaculty(request, pk):
    user = models.Faculty.objects.get(id=pk)
    form = forms.UserForm(instance=user)
    if (request.user.is_authenticated and request.user.is_staff) or (request.user.is_authenticated and request.user.role in [3,4]):
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated!")
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} updated account of {user.username}",
            )
            return redirect('admin-edit-profile', pk=user.id)
        else :
            for field, errors in form.errors.items():
                messages.error(request, '{}'.format(''.join(errors)))
            return redirect('admin-edit-profile', pk=user.id)
    context = {
        'form': form,
         'user' : user,
        'link' : redirect('department-head-faculty').url,
         "active" : "manage_department",
    }
    return render(request, 'edit_profile.html', context)

# RESEARCH COORDINATOR END


@login_required(login_url='anonymous')
def ResearchCoordinatorFaculty(request):
    if (request.user.is_authenticated and request.user.is_staff) or (request.user.is_authenticated and request.user.role in [2,4]):
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search)|
        Q(research__title__icontains = search) | 
        Q(research__status__status__iexact = search) 
    
        ).distinct().order_by('created_at')

    
    p = Paginator(faculty, 6)
    page = request.GET.get('page', 1)
    faculty = p.get_page(page)
    
    faculty_id = request.GET.get('faculty_id', 0)
    faculty_to_be_print = None
    if faculty_id != 0:
        faculty_to_be_print = models.Faculty.objects.get(id=faculty_id)
    
    researches = models.Research.objects.filter(user = faculty_id)
    status = models.ResearchStatus.objects.all()
    ctx = {
        "faculty" : faculty,
        "active" : "manage_research",
        'search' : search,
        'page' : page,
        'table_data' : researches,
        'faculty_id': faculty_id,
        'status' : status,
        'faculty_to_be_print' : faculty_to_be_print
    }
    
    return render(request, 'research_coordinator_faculty.html', ctx)



# EXTENSION COOR END

@login_required(login_url='anonymous')
def ExtensionCoordinatorFaculty(request):
    if (request.user.is_authenticated and request.user.is_staff) or (request.user.is_authenticated and request.user.role in [2,3]):
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    faculty = models.Faculty.objects.filter(
        Q(first_name__icontains = search) |
        Q(last_name__icontains = search)|
        Q(username__icontains = search)|
        Q(email__icontains = search)|
        Q(facultyextension__extension__title__iexact = search) 
    
        ).distinct().order_by('created_at')

    
    p = Paginator(faculty, 6)
    page = request.GET.get('page', 1)
    faculty = p.get_page(page)
    
    faculty_id = request.GET.get('faculty_id', 0)
    faculty_to_be_print = None
    if faculty_id != 0:
        faculty_to_be_print = models.Faculty.objects.get(id=faculty_id)
    extension = models.FacultyExtension.objects.filter(user = faculty_id)
    service = models.ExtensionService.objects.all()
    ctx = {
        "faculty" : faculty,
        "active" : "manage_extension",
        'search' : search,
        'page' : page,
        'table_data' : extension,
        'faculty_id': faculty_id,
        'service' : service,
        'faculty_to_be_print' : faculty_to_be_print
    }
    
    return render(request, 'extension_coordinator_faculty.html', ctx)




# POST ENDS

@login_required(login_url='anonymous')
def DepartmentHeadAnnouncement(request):
    form = forms.AnnouncementForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.category = request.user.department.title 
            announcement.save()
            messages.success(request, 'Post an announcement')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} post an announcement in {request.user.department.detail}",
            )
            return redirect('department-head-announcement')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    announcement = models.Announcement.objects.filter(
        Q(category = request.user.department.title) 
    
        ).distinct().order_by('-created_at')

    
    p = Paginator(announcement, 6)
    page = request.GET.get('page', 1)
    announcement = p.get_page(page)
    roles = [2]
    ctx = {
        "active" : "department_head_announcement",
        "form" : form,
        "label" : "Department",
        'table_data' : announcement,
        'roles': roles,
    }
    return render(request, 'all_announcement.html', ctx)


@login_required(login_url='anonymous')
def ResearchCoordinatorAnnouncement(request):
    form = forms.AnnouncementForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.category = "RESEARCH"
            announcement.save()
            messages.success(request, 'Post an announcement')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} post an announcement in RESEARCH",
            )
            return redirect('research-coordinator-announcement')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    announcement = models.Announcement.objects.filter(
        Q(category = "RESEARCH") 
    
        ).distinct().order_by('-created_at')

    
    p = Paginator(announcement, 6)
    page = request.GET.get('page', 1)
    announcement = p.get_page(page)
    roles = [3]
    ctx = {
        "active" : "research_coordinator_announcement",
        "form" : form,
        "label" : "Research",
        'table_data' : announcement,
        'roles': roles,
    }
    return render(request, 'all_announcement.html', ctx)


@login_required(login_url='anonymous')
def ExtensionCoordinatorAnnouncement(request):
    form = forms.AnnouncementForm()
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.category = "EXTENSION"
            announcement.save()
            messages.success(request, 'Post an announcement')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} post an announcement in EXTENSION",
            )
            return redirect('extension-coordinator-announcement')
    
    search =  request.GET.get('search') if request.GET.get('search') != None else ''
    announcement = models.Announcement.objects.filter(
        Q(category = 'EXTENSION') 
    
        ).distinct().order_by('-created_at')

    
    p = Paginator(announcement, 6)
    page = request.GET.get('page', 1)
    announcement = p.get_page(page)
    roles = [4]
    ctx = {
        "active" : "extension_coordinator_announcement",
        "form" : form,
        "label" : "Extension",
        'table_data' : announcement,
        'roles': roles,
    }
    return render(request, 'all_announcement.html', ctx)


@login_required(login_url='anonymous')
def EditAnnouncement(request, pk):
    announcement = models.Announcement.objects.get(id=pk)
    form = forms.AnnouncementForm(instance=announcement)
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    if request.method == 'POST':
        form = forms.AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated')
            models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} edited an announcement",
            )
            return redirect('edit-announcement', pk=announcement.id)
    link = ''    
    if request.user.is_authenticated and request.user.role == 2:
       link = redirect('department-head-announcement').url
    if request.user.is_authenticated and request.user.role == 3:
       link = redirect('research-coordinator-announcement').url   
    if request.user.is_authenticated and request.user.role == 4:
       link = redirect('extension-coordinator-announcement').url  
    
    ctx = {
        "active" : "",
        'form' : form,
        'label' : 'update',
        'link': link
    }
    return render(request, 'announcement_edit.html', ctx)
    
@login_required(login_url='anonymous')    
def DeleteAnnouncement(request, pk):
    
    link = ''    
    if request.user.is_authenticated and request.user.role == 2:
       link = redirect('department-head-announcement')
    if request.user.is_authenticated and request.user.role == 3:
       link = redirect('research-coordinator-announcement') 
    if request.user.is_authenticated and request.user.role == 4:
       link = redirect('extension-coordinator-announcement')
    
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Access denied, 403 forbidden page!")
        return redirect('logout')
    announcement = models.Announcement.objects.get(id = pk)
    if request.method == 'POST':
        
        messages.info(request, f"{announcement.username} is deleted.")
        models.ActivityLog.objects.create(
                    user = request.user,
                    action = f"{request.user.username} deleted activity log",
            )
        announcement.delete()
        return link
    
    ctx = {
        "obj": announcement,
        "active" : "admin_announcement",
        "label" : "Announcement",
        "link" : link.url
    }
    return render(request, 'all_delete.html', ctx)



# admin dashboard


def GetDashboardInformation(request):
    if request.method == 'GET':
           
        response_data = {}
        if request.user.is_authenticated and not request.user.is_staff:
            return JsonResponse({'success': False})
        # Faculty
        faculty_count = len(models.Faculty.objects.filter(role=1).order_by('created_at'))
        dept_head_count = len(models.Faculty.objects.filter(role=2).order_by('created_at'))
        research_coor_count = len(models.Faculty.objects.filter(role=3).order_by('created_at'))
        extension_count = len(models.Faculty.objects.filter(role=4).order_by('created_at'))
        
        faculty_data = {
            'faculty_count' : faculty_count,
            'dept_head_count' : dept_head_count,
            'research_coor_count' : research_coor_count,
            'extension_coor_count' : extension_count,
        }
        
        response_data['faculty_data'] = faculty_data
        
        # Research
        list_of_status = models.ResearchStatus.objects.all()
        
        research_data = []
        
        for status in list_of_status:
            data = {
                'x' : status.status,
                'value':len(status.research_set.all())
            }
            
            research_data.append(data)

        response_data['research_data'] = research_data
        
        
        
        # Extension
        
        
        list_of_extensions = models.ExtensionService.objects.all()
        
        extension_data = []
        
        for extension in list_of_extensions:
            
            data = {
                'x' : extension.title,
                'value':len(extension.facultyextension_set.all())
            }
            extension_data.append(data)
        
        response_data['extension_data'] = extension_data
        
        # Subject
        
        list_of_subjects = models.Subject.objects.all()
        
        subject_data = []
        
        for subject in list_of_subjects:
            data = {
                'x' : subject.title,
                'value':len(subject.facultysubject_set.all())
            }
            subject_data.append(data)

        
     
        response_data['subject_data'] = subject_data
        
        list_of_department = models.Department.objects.all()
        
        department_data = []
        
        for department in list_of_department:
            data = {
                'x' : department.title,
                'value':len(department.faculty_set.all())
            }
            department_data.append(data)
        
        response_data['department_data'] = department_data
        
        
        
        return JsonResponse(response_data)