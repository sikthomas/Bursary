from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'), 
    path('index', views.index, name='index'), 
    path('admin-index', views.adminindex, name='adminindex'),
    path('admin-index2', views.adminindex2, name='adminindex2'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login_view'), 
    path('logout/',views.logout_view, name='logout_view'),
    path('personalInformation', views.personalInformation, name='personalInformation'),
    path('institutionInformation', views.institutionInformation, name='institutionInformation'), 
    path('familyInformation', views.familyInformation, name='familyInformation'), 
    path('parent_type', views.parent_type, name='parent_type'), 
    path('additionalInformation/', views.additionalInformation, name='additionalInformation'),  
    path('applicant_list', views.applicant_list, name='applicant_list'), 
    path('applicant_details/<int:pk>/', views.applicant_details, name='applicant_details'),   
    path('pending_personalInformation/', views.pending_personalInformation, name='pending_personalInformation'),        
    path('pending_institutionInformation/', views.pending_institutionInformation, name='pending_institutionInformation'),        
    path('pending_parentInformation/', views.pending_parentInformation, name='pending_parentInformation'),  
    path('verify/<int:pk>/', views.verify_applicantion, name='verify_applicant'),
    path('verified/', views.verified_applications, name='verified_student'),  
    path('declined/', views.declined_applications, name='declined_applications'),   
    path('allocation/<int:pk>/', views.allocation, name='allocation'),  
    path('allocated/', views.allocated_list, name='allocated_list'),  
    path('role/', views.role, name='role'), 
    path('users/', views.systemUsers, name='users'), 
    path('delete/<int:pk>/', views.deleteUser, name='delete'), 


]