from django.urls import path,include
from . import views
app_name = 'base'

urlpatterns = [
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),

    path('index/', views.home, name='home'),
    path('index/room/<int:pk>', views.room, name='room'),
    path('create-room/', views.createRoom,  name='create-room'),
    path('update-room/<int:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>', views.deleteRoom, name='delete-room')

]

