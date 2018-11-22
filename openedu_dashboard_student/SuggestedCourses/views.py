from django.shortcuts import render
from use_function import namedtuplefetchall, getChooseDate
from django.db import connections
from suggest_course import suggest_course, suggested_by_age, suggested_by_education


def suggested_courses_view(request):
    request.encoding = 'utf-8'
    to_render = {}
    data = []
    output = []
    if request.method == 'GET':
        to_render = suggest_course(request)

    return render(request, 'SuggestedCourse.html', to_render)


def popular_courses_age_view(request):
    request.encoding = 'utf-8'
    to_render = {}
    data = []
    output = []
    if request.method == 'GET':
        to_render = suggested_by_age(request)

    return render(request, 'PopularCourseAge.html', to_render)


def popular_courses_education_view(request):
    request.encoding = 'utf-8'
    to_render = {}
    data = []
    output = []
    if request.method == 'GET':
        to_render = suggested_by_education(request)

    return render(request, 'PopularCourseEducation.html', to_render)


def ExistorNot(cid, course_data):
    exist = None
    for cd in course_data:
        if cd.course_id == cid:
            exist = [cd.課程代碼, cd.course_name]
            break

    return exist
