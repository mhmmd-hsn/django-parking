from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),


    path('', views.home, name='home'),
    path('all_customers/',views.AllCustomers , name = 'all_customers'),
    path('parking_data/',views.ParkingData , name = 'parking_data'),
    path('change_capacity/', views.ChangeCapacity, name="change_capacity"),
    path('set_admin/<str:pk>', views.SetAsAdmin, name="set_admin"),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

    path('delete_event/<str:pk>/', views.DeleteEvent, name='delete_event'),
    path('create_event/<str:pk>/', views.CreateEvent, name='create_event'),
    path('create_event_exit/<str:pk>/', views.ExitEvent, name='create_event_exit'),
]