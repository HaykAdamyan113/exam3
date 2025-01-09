from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Rating
from .forms import RatingForm, UserRegistrationForm, CourseForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            new_rating = form.cleaned_data['new_rating']
            course.update_rating(new_rating)
            return redirect('course_detail', course_id=course.id)
    else:
        form = RatingForm()
    return render(request, 'courses/course_detail.html', {'course': course, 'form': form})

@login_required
def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        rate = request.POST.get('rate') 
        count = request.POST.get('count')
        
        
        course = Course.objects.create(
            title=title,
            description=description,
            average_rating = rate,
            rating_count = count
        )
        return redirect('course_list') 
    return render(request, 'courses/add_course.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('course_list') 
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})

@login_required
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('course_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('course_list')


@login_required
def rate_course(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
           
            rating = form.cleaned_data['rating']

            
            if rating < 0:
                rating = 0
            elif rating > 10:
                rating = 10

       
            new_rating = (course.rating * course.rating_count + rating) / (course.rating_count + 1)
            course.rating = new_rating
            course.rating_count += 1
            course.save()

            
            return redirect('course_list')


    else:
        form = RatingForm()


    return render(request, 'courses/rate_course.html', {'form': form, 'course': course})