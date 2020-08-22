from django.urls import path
from . import views


urlpatterns = [
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),

    path('', views.index, name="index"),
    path('newinvoice/', views.newinvoice, name="newinvoice"),
    path('loadinvoice/', views.loadinvoice, name="loadinvoice"),
    path('fillinvoice/', views.fillinvoice, name="fillinvoice"),
    path('fillindetails/', views.fillindetails, name="fillindetails"),
    path('saveindetails/', views.saveindetails, name="saveindetails"),
    path('viewagentinvoice/', views.viewagentinvoice, name="viewagentinvoice"),
    path('viewallinvoices/', views.viewallinvoices, name="viewallinvoices"),
]