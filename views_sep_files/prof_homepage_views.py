from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime


def prof_login(request):
    context = {}
    if 'error_message' in request.session.keys():
        context['error_message'] = request.session['error_message']

    if 'valid_username' in request.session.keys():
        context['valid_username'] = request.session['valid_username']

    return render(request, 'eval/prof-login.html', context=context)


def check_login(request):
    username = request.POST.get('username', '') # If no username, default='blank-username'
    password = request.POST.get('password', '') # If no password, default='blank-pswd'

    try:
        professor = Professor.objects.get(prof_id=username)
        if password == professor.prof_pswd:
            request.session['prof_id'] = username
            return redirect('/prof-homepage')

    except (KeyError, Professor.DoesNotExist):
        request.session['error_message'] = "Invalid username"
        return redirect('/prof-login')


    request.session['error_message'] = "Password incorrect"
    request.session['valid_username'] = username
    return redirect('/prof-login')


def prof_homepage(request):
    if 'prof_id' not in request.session.keys():
        return redirect('/prof-login')

    professor = Professor.objects.get(prof_id=request.session['prof_id'])

    courses  = SemesterCourse.objects.filter(prof_id=professor).order_by('-semester_end_date')

    if 'error_message' in request.session:
        error_message = request.session['error_message']
        del request.session['error_message']
    else:
        error_message = ""


    if 'confirm_message' in request.session:
        confirm_message = request.session['confirm_message']
        del request.session['confirm_message']
    else:
        confirm_message = ""

    return render(request, 'eval/prof-homepage.html', {
        'professor' : professor,
        'courses' : courses,
        'error_message' : error_message,
        'confirm_message' : confirm_message,
        })

def edit_course_action(request):
    course_id = request.POST.get('course-id', '')
    if not course_id:
        return redirect('/prof-homepage')

    request.session['course-id'] = course_id
    if 'edit-course' in request.POST:
        return redirect('/edit-course')
    elif 'delete-course' in request.POST:
        return redirect('/delete-course')
    else:
        return redirect('/prof-homepage')
