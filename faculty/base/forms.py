from django.forms import ModelForm
from django.forms.models import apply_limit_choices_to_to_formfield
from base import models
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = models.Faculty
        fields = ['first_name', 'last_name', 'username', 'email','address', 'password1', 'password2', 'emp_no', 
                  'contact_no', 'department',]
              
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter last name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'Enter username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Enter email'})
        self.fields['address'].widget.attrs.update({'class': 'form-control','placeholder':'Enter location (optional)'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':'Confirm password'})
        self.fields['emp_no'].widget.attrs.update({'class': 'form-control','placeholder':'Enter employee no.'})
        self.fields['contact_no'].widget.attrs.update({'class': 'form-control','placeholder':'Enter contact no.'})
        self.fields['department'].widget.attrs.update({'class': 'form-control','placeholder':'Choose department'})
        
class UserForm(ModelForm):
    class Meta:
        model = models.Faculty
        fields = ['avatar', 'first_name','last_name','username',  'email', 'address', 'emp_no', 'contact_no', 'department']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter last name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'Enter username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Enter email'})
        self.fields['address'].widget.attrs.update({'class': 'form-control','placeholder':'Enter location (optional)'})
        self.fields['emp_no'].widget.attrs.update({'class': 'form-control','placeholder':'Enter employee no.'})
        self.fields['contact_no'].widget.attrs.update({'class': 'form-control','placeholder':'Enter contact no.'})
        self.fields['department'].widget.attrs.update({'class': 'form-control','placeholder':'Choose department'})
        
        
        self.fields['first_name'].widget.attrs['required'] = 'required'
        self.fields['last_name'].widget.attrs['required'] = 'required'
        self.fields['username'].widget.attrs['required'] = 'required'
        self.fields['email'].widget.attrs['required'] = 'required'
        self.fields['emp_no'].widget.attrs['required'] = 'required'
        self.fields['contact_no'].widget.attrs['required'] = 'required'
        self.fields['department'].widget.attrs['required'] = 'required'
        
        
class SubjectForm(ModelForm):
    class Meta:
        model = models.Subject
        fields = ['title', 'code', 'units']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['code'].widget.attrs.update({'class': 'form-control','placeholder':'Enter code'})
        self.fields['units'].widget.attrs.update({'class': 'form-control','placeholder':'Enter units'})
       
       
       
        self.fields['title'].widget.attrs['required'] = 'required'
        self.fields['code'].widget.attrs['required'] = 'required'
        self.fields['units'].widget.attrs['required'] = 'required'
       
       
       
class ResearchFormWithUser(ModelForm):
    class Meta:
        model = models.Research
        fields = ['user', 'title', 'file', 'detail', 'content', 'status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['title'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['file'].widget.attrs.update({'class': 'form-control','placeholder':'Enter file'})
        self.fields['detail'].widget.attrs.update({'class': 'form-control','placeholder':'Enter detail'})
        self.fields['content'].widget.attrs.update({'class': 'form-control','placeholder':'Enter content'})
        self.fields['status'].widget.attrs.update({'class': 'form-control','placeholder':'Enter status'})
       
       
       
        self.fields['user'].widget.attrs['required'] = 'required'
        self.fields['title'].widget.attrs['required'] = 'required'
        # self.fields['file'].widget.attrs['required'] = 'required'
        self.fields['detail'].widget.attrs['required'] = 'required'
        self.fields['content'].widget.attrs['required'] = 'required'
        self.fields['status'].widget.attrs['required'] = 'required'
        
        
class ResearchFormNoUser(ModelForm):
    class Meta:
        model = models.Research
        fields = [ 'title', 'file', 'detail', 'content', 'status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['file'].widget.attrs.update({'class': 'form-control','placeholder':'Enter file'})
        self.fields['detail'].widget.attrs.update({'class': 'form-control','placeholder':'Enter detail'})
        self.fields['content'].widget.attrs.update({'class': 'form-control','placeholder':'Enter content'})
        self.fields['status'].widget.attrs.update({'class': 'form-control','placeholder':'Enter status'})
       
       
       
        self.fields['title'].widget.attrs['required'] = 'required'
        # self.fields['file'].widget.attrs['required'] = 'required'
        self.fields['detail'].widget.attrs['required'] = 'required'
        self.fields['content'].widget.attrs['required'] = 'required'
        self.fields['status'].widget.attrs['required'] = 'required'
        
        
        

class ExtensionServiceForm(ModelForm):
    class Meta:
        model = models.ExtensionService
        fields = ['title', 'detail']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['detail'].widget.attrs.update({'class': 'form-control','placeholder':'Enter detail about this extension'})
       
    
        self.fields['title'].widget.attrs['required'] = 'required'
        self.fields['detail'].widget.attrs['required'] = 'required'
        
class ProjectForm(ModelForm):
    
    class Meta:
        model = models.Project
        fields = [ 'project_detail']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

     
        self.fields['project_detail'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'Enter project under this extension',
            'style': 'height: 100px;',
            })
       
        
    
        self.fields['project_detail'].widget.attrs['required'] = 'required'
        
        
class FacultySubjectForm(ModelForm):
    
    class Meta:
        model = models.FacultySubject
        fields = [ 'subject']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    
        self.fields['subject'].widget.attrs['required'] = 'required'
        
        self.fields['subject'].widget.attrs.update({'class': 'form-control','placeholder':'Enter title'})
        self.fields['subject'].queryset = models.Subject.objects.filter(is_preset=True)  
        

class FacultyExtensionForm(ModelForm):
    
    class Meta:
        model = models.FacultyExtension
        fields = [ 'extension']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    
        self.fields['extension'].widget.attrs['required'] = 'required'
        
        self.fields['extension'].widget.attrs.update({'class': 'form-control','placeholder':'Enter extension'})
        self.fields['extension'].queryset = models.ExtensionService.objects.filter(is_preset=True)  
      
class AnnouncementForm(ModelForm):
    
    class Meta:
        model = models.Announcement
        fields = [ 'content']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    
        self.fields['content'].widget.attrs['required'] = 'required'
        
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'Announcement something...',
            'style': 'height: 150px;',
            })