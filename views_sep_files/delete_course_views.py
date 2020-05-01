from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime


def delete_course(request):
    course = SemesterCourse.objects.get(pk=request.session['course-id'])
    weekly_eval_times = SemesterCourseEvalTime.objects.filter(semester_course_id=course)
    days_of_week = [("Sunday", 1),
                    ("Monday", 2),
                    ("Tuesday", 3),
                    ("Wednesday", 4),
                    ("Thursday", 5),
                    ("Friday", 6),
                    ("Saturday", 7)
                    ]

    return render(request, 'eval/delete-course.html', {
        'course' : course,
        'semesters' : ['Fall', 'January', 'Spring', 'Summer'],
        'semester_start_date' : course.semester_start_date.strftime('%Y-%m-%d'),
        'semester_end_date' : course.semester_end_date.strftime('%Y-%m-%d'),
        'weekly_eval_times' : weekly_eval_times,
        'days_of_week' : days_of_week,
    })


def submit_delete_course(request):
    course = SemesterCourse.objects.get(pk=request.session['course-id'])
    del request.session['course-id']

    course.delete()

    return redirect('/prof-homepage')
