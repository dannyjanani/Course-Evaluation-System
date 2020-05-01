from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime


def edit_course(request):
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

    return render(request, 'eval/edit-course.html', {
        'course' : course,
        'semesters' : ['Fall', 'January', 'Spring', 'Summer'],
        'semester_start_date' : course.semester_start_date.strftime('%Y-%m-%d'),
        'semester_end_date' : course.semester_end_date.strftime('%Y-%m-%d'),
        'weekly_eval_times' : weekly_eval_times,
        'days_of_week' : days_of_week,

    })


def submit_edit_course(request):
    course = SemesterCourse.objects.get(pk=request.session['course-id'])
    del request.session['course-id']

    course_num = request.POST.get('course-number')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    semester_start_date = request.POST.get('semester-start')
    semester_end_date = request.POST.get('semester-end')
    max_num_meeting_times = request.POST.get('max-meeting-time')

    if not (course_num and semester and year and semester_start_date and semester_end_date):
        request.session['error_message'] = "Course information incomplete. Changes not saved."
        return redirect('/prof-homepage')

    if semester_start_date > semester_end_date:
        request.session['error_message'] = "Course information incomplete. New course not saved."
        return redirect('/prof-homepage')

    course.course_num = course_num
    course.semester = semester
    course.year = year
    course.semester_start_date = semester_start_date
    course.semester_end_date = semester_end_date

    course.save()

    old_eval_times = SemesterCourseEvalTime.objects.filter(semester_course_id=course)
    for old_time in old_eval_times:
        old_time.delete()

    for i in range(1, int(max_num_meeting_times)+1):
        day = request.POST.get("day-"+str(i))
        start_time = request.POST.get("start-time-"+str(i))
        end_time = request.POST.get("end-time-"+str(i))

        if day and start_time and end_time:
            eval_time = SemesterCourseEvalTime(semester_course_id=new_course, day_of_week=day, start_time=start_time, end_time=end_time)
            if (eval_time.start_time < eval_time.end_time):
                eval_time.save()

    request.session['confirm_message'] = "Your changes have been saved."
    return redirect('/prof-homepage')
