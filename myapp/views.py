from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login
from myapp.models import BlogPost

# Create your views here.
def signupform(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('user_type')
        if password == confirm_pass:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signupform')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signupform')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                user_profile = UserProfile.objects.create(user=user, address_line1=address_line1,
                                                           city=city, state=state, pincode=pincode,profile_picture=profile_picture)
                
                # Set user_type based on the selected radio button
                if user_type == 'patient':
                    user_profile.is_patient = True
                elif user_type == 'doctor':
                    user_profile.is_doctor = True
                    
                user_profile.save()
                return redirect('loginform')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signupform')
    return render(request,'myapp/sighupform.html')

def loginform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.is_patient:
                    return redirect('patient_dashboard')
                elif user_profile.is_doctor:
                    return redirect('doctor_dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found')
                return redirect('loginform')    
        else:
            messages.error(request,'Invalid username or password')
            return redirect('loginform')
    return render(request,'myapp/loginform.html')

def doctor_dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile does not exist
        user_profile = None
    return render(request,'myapp/doctor_dashboard.html',{'user_profile': user_profile})

def patient_dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile does not exist
        user_profile = None
    return render(request,'myapp/patient_dashboard.html',{'user_profile': user_profile})

def blog_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        
        blog_obj = BlogPost(
            title=title,
            image=image,
            category=category,
            summary=summary,
            content=content
        )
        blog_obj.save()
        return redirect('blog_list')
    return render(request,'myapp/blog_form.html')

def blog_detail(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        e = request.FILES.get('image')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
    
        blog_detail = BlogPost.objects.get(pk=title)
        blog_detail.title = title,
        blog_detail.image=image,
        blog_detail.category=category,
        blog_detail.summary=summary,
        blog_detail.content=content,
        blog_detail.save()
    add_post = get_object_or_404(BlogPost, pk=id)
    context={
        'add_post':add_post,
    }
        
    return render(request, 'myapp/blog_detail.html',context)

def blog_list(request):
    blogs = BlogPost.objects.all()
    context ={
        'blogs':blogs,
    }
    return render(request,'myapp/blog_list.html',context)



