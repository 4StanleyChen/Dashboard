from django.shortcuts import render
from django.db import connections, DatabaseError
from collections import namedtuple
from use_function import namedtuplefetchall


# Create your views here.
def test1_view(request):
    to_render = {}

    with connections['ResultDB'].cursor() as cursor:
        # 搜尋所有修同一課程之學生
        course_id = 'course-v1:FCUx+2015015+201512'
        cursor.execute(
            "SELECT distinct(user_id) as uid FROM edxresult.student_total_data WHERE course_id = %s", [course_id]
        )
        result = namedtuplefetchall(cursor)

        n = 0
        for rs in result:
            to_render['ttt'] = type(result)

        print(type(result))

    return render(request, 'test1.html', to_render)
