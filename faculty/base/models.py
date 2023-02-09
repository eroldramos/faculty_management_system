from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=200,unique = True,)
    detail = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(f"{self.title}")

#0-admin, 1-faculty, 2-depthead, 3-research coor, 4-ext coor    
class Faculty(AbstractUser):
    email = models.EmailField(unique = True, null=True)
    avatar = CloudinaryField(resource_type="image", null=True, blank=False)
    emp_no = models.CharField(max_length=25, unique=True, null=True)
    contact_no = models.CharField(max_length=20, unique=True, null=True)
    role = models.IntegerField(default=0) 
    address = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    def __str__(self):
        return str(f"{self.first_name} {self.last_name}")
    
class ActivityLog(models.Model):
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    action = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f"{self.action}")
    class Meta:
        ordering = ['-created_at']
        
#  research table
class ResearchStatus(models.Model):
    status = models.CharField(max_length=200)
    def __str__(self):
        return str(f"{self.status}")
    class Meta:
        ordering = ['id']
        
        
class Research(models.Model):
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    file = CloudinaryField(resource_type="auto", null=True, blank=False)
    filename = models.CharField(max_length=200, null=True)
    detail = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    is_publish = models.BooleanField(default=False, verbose_name="Publish") 
    status = models.ForeignKey(ResearchStatus, on_delete=models.SET_NULL, null=True, blank=True) # ongoing, presented, published
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    def __str__(self):
        return str(f"{self.title}")
    
# extension table
class ExtensionService(models.Model):
    title = models.CharField(max_length=200, null=True)
    detail = models.TextField(null=True, blank=True)
    is_preset = models.BooleanField(default=True, verbose_name="admin-extensions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    def __str__(self):
        return str(f"{self.title}")
    
    
# extension project
class Project(models.Model):
    extension = models.ForeignKey(ExtensionService, on_delete=models.CASCADE)
    project_detail = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(f"{self.project_detail}")
# faculty extension  
class FacultyExtension(models.Model):
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    extension = models.ForeignKey(ExtensionService, on_delete=models.CASCADE, null=True)
         
# Announcement table
class Announcement(models.Model):
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    def __str__(self):
        return str(f"{self.content}")
# subject table

class Subject(models.Model):
    title = models.CharField(max_length=200, unique=True, null=True, blank=True) 
    code = models.CharField(max_length=200, unique=True, null=True, blank=True)
    units = models.IntegerField(default=0, null=True)
    is_preset = models.BooleanField(default=True, verbose_name="admin-subjects")
    def __str__(self):
        return str(f"{self.title}")
    
    
# faculty subject
class FacultySubject(models.Model):
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)