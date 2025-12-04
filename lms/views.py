from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Course, Enrollment

def register(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        u, e, p, r = request.POST.get('username'), request.POST.get('email'), request.POST.get('password'), request.POST.get('role', 'student')
        if User.objects.filter(username=u).exists() or User.objects.filter(email=e).exists():
            messages.error(request, 'Username or email already exists')
        else:
            login(request, User.objects.create_user(username=u, email=e, password=p, role=r))
            return redirect('dashboard')
    return render(request, 'lms/register.html')

def user_login(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user: login(request, user); return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'lms/login.html')

@login_required
def user_logout(request):
    logout(request); return redirect('user_login')

@login_required
def dashboard(request):
    is_instructor = request.user.role == 'instructor'
    if is_instructor:
        courses = Course.objects.filter(instructor=request.user)
        # Count unique students across all instructor's courses
        total_students = Enrollment.objects.filter(course__instructor=request.user).values('student').distinct().count()
        return render(request, 'lms/instructor_dashboard.html', {'courses': courses, 'total_students': total_students})
    else:
        return render(request, 'lms/student_dashboard.html', {
            'enrollments': Enrollment.objects.filter(student=request.user),
            'available_courses': Course.objects.exclude(enrollments__student=request.user)
        })

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.bio, request.user.email = request.POST.get('bio', ''), request.POST.get('email', request.user.email)
        request.user.save(); messages.success(request, 'Profile updated!'); return redirect('profile')
    return render(request, 'lms/profile.html')

@login_required
def course_create(request):
    if request.user.role != 'instructor': return redirect('dashboard')
    if request.method == 'POST':
        Course.objects.create(title=request.POST.get('title'), description=request.POST.get('description'), instructor=request.user)
        return redirect('dashboard')
    return render(request, 'lms/course_form.html')

@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.title, course.description = request.POST.get('title'), request.POST.get('description')
        course.save(); messages.success(request, 'Course updated!'); return redirect('dashboard')
    return render(request, 'lms/course_form.html', {'course': course})

@login_required
def enroll_course(request, course_id):
    if request.user.role == 'student': Enrollment.objects.get_or_create(student=request.user, course=get_object_or_404(Course, id=course_id))
    return redirect('dashboard')

@login_required
def course_delete(request, course_id):
    get_object_or_404(Course, id=course_id, instructor=request.user).delete(); messages.success(request, 'Course deleted!'); return redirect('dashboard')
