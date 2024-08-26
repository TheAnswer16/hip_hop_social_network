from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from app.cloudinary import Cloudinary

from app.models import *

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
        messages.error(request, 'Credenciais inválidas, por favor tente novamente.')
        return render(request, 'login.html', {'error': 'Credenciais inválidas'})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
                
        user = User.objects.create_user(username=username, password=password, full_name=full_name, gender=gender)
        user.save()
        login(request, user)    
        return redirect('home')
@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home.html', {'posts': posts})
    
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')
    
    def post(self, request):
        user = request.user
        user.full_name = request.POST.get('full_name')
        user.save()
        return redirect('profile')
    
class EditProfile(View):
    def get(self, request):
        return render(request, 'edit_profile.html')
    
    def post(self, request):
        user = request.user
        user.full_name = request.POST.get('full_name')
        user.bio = request.POST.get('bio')
        user.profile_picture = request.FILES.get('profile_picture')
        user.instagram = request.POST.get('instagram')
        user.twitter = request.POST.get('twitter')
        user.spotify = request.POST.get('spotify')
        user.youtube = request.POST.get('youtube')
        user.save()
        return redirect('profile')
    
class PostView(View):
    def get(self, request):
        return render(request, 'post.html')
    
    def post(self, request):
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        text_content = request.POST.get('text_content')
        link = request.POST.get('link')
        print(request.FILES.get('image'))
        image = Cloudinary.upload(request.FILES.get('image'), "image_" + title)
        user = request.user
        
        post = Post.objects.create(title=title, subtitle=subtitle, text_content=text_content, link=link, image=image, user=user)
        post.save()
        return redirect('home')
    
