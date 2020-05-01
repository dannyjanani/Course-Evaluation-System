from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from datetime import datetime

def add_course(request):
    return render(request, 'eval/add-course.html', {})


def submit_add_course(request):
    course_num = request.POST.get('course-number')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    semester_start = request.POST.get('semester-start')
    semester_end = request.POST.get('semester-end')
    max_num_meeting_times = request.POST.get('max-meeting-time')

    if semester_start > semester_end:
        request.session['error_message'] = "Course information incomplete. New course not saved."
        return redirect('/prof-homepage')

    new_course = SemesterCourse()

    new_course.prof_id = Professor.objects.get(pk=request.session['prof_id'])
    new_course.course_num = course_num
    new_course.semester = semester
    new_course.year = year
    new_course.semester_start_date = semester_start
    new_course.semester_end_date = semester_end
    new_course.save()

    for i in range(1, int(max_num_meeting_times)+1):
        day = request.POST.get("day-"+str(i))
        start_time = request.POST.get("start-time-"+str(i))
        end_time = request.POST.get("end-time-"+str(i))
        if day and start_time and end_time:
            eval_time = SemesterCourseEvalTime(semester_course_id=new_course, day_of_week=day, start_time=start_time, end_time=end_time)
            if (eval_time.start_time < eval_time.end_time):
                eval_time.save()

    request.session['confirm_message'] = "A new course has been added successfully"
    return redirect('/prof-homepage')
