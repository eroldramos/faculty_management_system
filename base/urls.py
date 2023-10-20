from django.urls import path
from . import views

urlpatterns = [

    path('anonymous-user', views.PleaseLoginToAccessThisPage, name = 'anonymous'),
    path('register',views.RegisterPage, name="register"),
    path('password-reset',views.PasswordReset, name="password-reset"),
    path('',views.LoginPage, name="login"),
    path('logout',views.LogoutUser, name="logout"),
    path('edit-profile',views.EditProfile, name="edit-profile"),
    path('admin-dashboard',views.AdminDashboard, name="admin-dashboard"),
    path('admin-faculty',views.AdminFaculty, name="admin-faculty"),
    path('admin-department',views.AdminDepartmentHead, name="admin-department"),
    path('admin-research',views.AdminResearchCoordinator, name="admin-research"),
    path('admin-extension',views.AdminExtensionCoordinator, name="admin-extension"),
    path('admin-subject',views.AdminSubject, name="admin-subject"),
    path('admin-add-subject',views.AdminAddSubject, name="admin-add-subject"),
    path('admin-researches',views.AdminResearches, name="admin-researches"),
    path('admin-add-research',views.AdminAddResearch, name="admin-add-research"),
    path('admin-extension-service',views.AdminExtensionService, name="admin-extension-service"),
    path('admin-add-extension-service',views.AdminAddExtensionService, name="admin-add-extension-service"),
    path('admin-activitylog',views.AdminActivityLog, name="admin-activitylog"),
    
    
    
    path('faculty-research',views.FacultyResearch, name="faculty-research"),
    path('faculty-add-research',views.FacultyAddResearch, name="faculty-add-research"),
    path('faculty-my-research',views.FacultyMyResearch, name="faculty-my-research"),
    path('faculty-add-preset-subject',views.FacultyAddPresetSubject, name="faculty-add-preset-subject"),
    path('faculty-add-own-subject',views.FacultyAddOwnSubject, name="faculty-add-own-subject"),
    path('faculty-subject',views.FacultySubject, name="faculty-subject"),
    path('faculty-extension-service',views.FacultyExtensionService, name="faculty-extension-service"),
    path('faculty-add-preset-extension-service',views.FacultyAddPresetExtensionService, name="faculty-add-preset-extension-service"),
    path('faculty-add-own-extension-service',views.FacultyAddOwnExtensionService, name="faculty-add-own-extension-service"),
    
    
    
    path('department-head-faculty',views.DepartmentHeadFaculty, name="department-head-faculty"),
    path('department-head-announcement',views.DepartmentHeadAnnouncement, name="department-head-announcement"),
    
    
    path('research-coordinator-faculty',views.ResearchCoordinatorFaculty, name="research-coordinator-faculty"),
    path('research-coordinator-announcement',views.ResearchCoordinatorAnnouncement, name="research-coordinator-announcement"),
   
    path('extension-coordinator-faculty',views.ExtensionCoordinatorFaculty, name="extension-coordinator-faculty"),
    path('extension-coordinator-announcement',views.ExtensionCoordinatorAnnouncement, name="extension-coordinator-announcement"),
   
   
   
    path('get-dashboard-information',views.GetDashboardInformation, name="get-dashboard-information"),
    
    
    
    
    
    path('change-role/<str:pk>/<str:num>/<str:department>',views.ChangeRole, name="change-role"),
    path('admin-edit-profile/<str:pk>',views.AdminEditProfile, name="admin-edit-profile"),
    path('admin-delete-faculty/<str:pk>',views.AdminDeleteFaculty, name="admin-delete-faculty"),
    path('admin-edit-subject/<str:pk>',views.AdminEditSubject, name="admin-edit-subject"),
    path('admin-delete-subject/<str:pk>',views.AdminDeleteSubject, name="admin-delete-subject"),
    path('admin-edit-research/<str:pk>',views.AdminEditResearch, name="admin-edit-research"),
    path('admin-delete-research/<str:pk>',views.AdminDeleteResearch, name="admin-delete-research"),
    path('delete-project/<str:pk>',views.DeleteProject, name="delete-project"),
    path('admin-edit-extension-service/<str:pk>',views.AdminEditExtensionService, name="admin-edit-extension-service"),
    path('admin-delete-extension-service/<str:pk>',views.AdminDeleteExtensionService, name="admin-delete-extension-service"),
    path('admin-delete-activitylog/<str:pk>',views.AdminDeleteActivityLog, name="admin-delete-activitylog"),




    path('faculty-edit-research/<str:pk>',views.FacultyEditResearch, name="faculty-edit-research"),
    path('faculty-delete-research/<str:pk>',views.FacultyDeleteResearch, name="faculty-delete-research"),
    path('faculty-research-detail/<str:pk>',views.FacultyResearchDetail, name="faculty-research-detail"),
    path('faculty-edit-subject/<str:pk>',views.FacultyEditSubject, name="faculty-edit-subject"),
    path('faculty-delete-subject/<str:pk>',views.FacultyDeleteSubject, name="faculty-delete-subject"),   
    path('faculty-edit-extension-service/<str:pk>',views.FacultyEditExtensionService, name="faculty-edit-extension-service"),   
    path('faculty-delete-extension-service/<str:pk>',views.FacultyDeleteExtensionService, name="faculty-delete-extension-service"),   
    
    
    
    path('department-head-edit-faculty/<str:pk>',views.DepartmentHeadEditFaculty, name="department-head-edit-faculty"),    
    
    
    path('edit-announcement/<str:pk>',views.EditAnnouncement, name="edit-announcement"),    
    path('delete-announcement/<str:pk>',views.DeleteAnnouncement, name="delete-announcement"),    
    
    
    
    
    
]
