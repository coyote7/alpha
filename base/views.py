from django.shortcuts import render
from .models import *
from .forms import RoomForm
from django. shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
#add decoraters to restrict views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#user registration
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def loginpage(request):
    page ='login'
    if request.user.is_authenticated :
        return  redirect('base:home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username =username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')

        else:
            messages.error(request, "Username or password does not exist")
    context = {'page':page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')

def registerUser(request):
    page='register'
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user) # auto login user
            redirect('base:home')
        else:
            messages.error(request,"an issue with your login..check conditions")

    return render(request,'base/login_register.html',{'form':form})



def home(request):
    q = request.GET.get('q')
   # rooms = Room.objects.filter(topic__name__icontains
                               # =q)
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    detail = Room.objects.all()
    room = Room.objects.get(id=pk)
    context = {'room': room,'detail':detail}
    return render(request, 'base/room.html', context)


@login_required(login_url='base:login')
def createRoom(request):
    text = "Create form "
    form = RoomForm()
    context = {'text': text,'form': form }
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            print("Valid ..addedd succesfully")
            return redirect('base:home')
        print(request.POST)
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user !=room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            print("Edited ... succesfully")
            return redirect('base:home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base:login')

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this post")
    if request.method ==  'POST':
        room.delete()
        return redirect('base:home')
    return render(request,'base/delete.html',{'obj':room})
