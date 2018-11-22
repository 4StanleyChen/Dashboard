from use_function import namedtuplefetchall, getChooseDate
from django.db import connections


def suggest_course(request):
    request.encoding = 'utf-8'
    to_render = {}
    data = []
    output = []

    with connections['ResultDB'].cursor() as cursor:
        # 搜尋所有修同一課程之學生
        course_id = 'course-v1:FCUx+2015015+201512'
        cursor.execute(
            "SELECT distinct(user_id) FROM student_total_data0912 WHERE course_id = %s", [course_id]
        )
        users = namedtuplefetchall(cursor)

        # 所有學生修課資料
        cursor.execute(
            "SELECT course_id, user_id FROM student_total_data0912"
        )
        courses = namedtuplefetchall(cursor)

        # 課程資料
        cursor.execute(
            "SELECT distinct(course_id), course_name,課程代碼 FROM course_total_data_v2"
        )
        course_data = namedtuplefetchall(cursor)

        student_count = {}
        for user in users:
            for course in courses:
                if course.user_id == user.user_id:
                    if course.course_id in student_count:
                        student_count[course.course_id] += 1
                    else:
                        student_count[course.course_id] = 1

        # 排序
        student_count = dict(sorted(student_count.items(), key=lambda x: x[1], reverse=True))

        # 計算人數
        total_user = 0
        for value in student_count.values():
            total_user += value

        temp = []
        c = 0
        for key, value in student_count.items():
            temp.clear()
            check = ExistorNot(key, course_data)
            if c < 5:
                if check is not None:
                    temp.append(check[0])
                    temp.append(check[1])
                    temp.append(check[2])
                    temp.append(value)
                    temp.append(str(int(value / total_user * 100)) + '%')
                    output.append(temp.copy())
                    c += 1

            else:
                break

        cursor.execute("SELECT course_name FROM course_total_data_v2 WHERE course_id = %s", [course_id])
        result = namedtuplefetchall(cursor)

        CourseName = result[-1].course_name

        to_render['data'] = output
        to_render['CourseName'] = CourseName

        return to_render


def suggested_by_age(request):
    to_render = {}

    with connections['ResultDB'].cursor() as cursor:
        cursor.execute(
            "SELECT 課程代碼, course_id, course_name, age_17, age_18_25, age_26_ FROM course_total_data_v2"
        )
        result = namedtuplefetchall(cursor)

        max_17 = 0
        max_18_25 = 0
        max_26_ = 0
        total_17 = 0
        total_18_25 = 0
        total_26_ = 0

        output_17 = ['' for i in range(4)]
        output_18_25 = ['' for i in range(4)]
        output_26_ = ['' for i in range(4)]

        for rs in result:
            totalage = rs.age_17 + rs.age_18_25 + rs.age_26_

            if max_17 < rs.age_17:
                max_17 = rs.age_17
                total_17 = totalage
                output_17[0] = rs.課程代碼
                output_17[1] = rs.course_id
                output_17[2] = rs.course_name
                output_17[3] = str(max_17)
            elif max_17 == rs.age_17:
                if total_17 > totalage:
                    output_17[0] = rs.課程代碼
                    output_17[1] = rs.course_id
                    output_17[2] = rs.course_name
                    output_17[3] = str(max_17)

            if max_18_25 < rs.age_18_25:
                max_18_25 = rs.age_18_25
                total_18_25 = totalage
                output_18_25[0] = rs.課程代碼
                output_18_25[1] = rs.course_id
                output_18_25[2] = rs.course_name
                output_18_25[3] = str(max_18_25)
            elif max_18_25 == rs.age_18_25:
                if total_18_25 > totalage:
                    output_18_25[0] = rs.課程代碼
                    output_18_25[1] = rs.course_id
                    output_18_25[2] = rs.course_name
                    output_18_25[3] = str(max_18_25)

            if max_26_ < rs.age_26_:
                max_26_ = rs.age_26_
                total_26_ = totalage
                output_26_[0] = rs.課程代碼
                output_26_[1] = rs.course_id
                output_26_[2] = rs.course_name
                output_26_[3] = str(max_26_)
            elif max_26_ == rs.age_26_:
                if total_26_ > totalage:
                    output_26_[0] = rs.課程代碼
                    output_26_[1] = rs.course_id
                    output_26_[2] = rs.course_name
                    output_26_[3] = str(max_26_)

        to_render['output_26_'] = output_26_
        to_render['output_18_25'] = output_18_25
        to_render['output_17'] = output_17

        return to_render


def suggested_by_education(request):
    to_render = {}
    with connections['ResultDB'].cursor() as cursor:
        cursor.execute(
            "SELECT 課程代碼, course_id, course_name, 博士, 碩士, 學士, 副學士, 高中, 國中, 國小 FROM course_total_data_v2"
        )
        result = namedtuplefetchall(cursor)

        max_p = max_m = max_b = max_a = max_hs = max_jhs = max_el = 0
        totalall = 0
        total_p = total_m = total_b = total_a = total_hs = total_jhs = total_el = 0
        output_p = ['' for i in range(4)]
        output_m = ['' for i in range(4)]
        output_b = ['' for i in range(4)]
        output_a = ['' for i in range(4)]
        output_hs = ['' for i in range(4)]
        output_jhs = ['' for i in range(4)]
        output_el = ['' for i in range(4)]

        for rs in result:
            totalall = rs.博士 + rs.碩士 + rs.學士 + rs.副學士 + rs.高中 + rs.國中 + rs.國小

            if max_p < rs.博士:
                max_p = rs.博士
                total_p = totalall
                output_p[0] = rs.課程代碼
                output_p[1] = rs.course_id
                output_p[2] = rs.course_name
                output_p[3] = rs.博士
            elif max_p == rs.博士:
                if total_p > totalall:
                    output_p[0] = rs.課程代碼
                    output_p[1] = rs.course_id
                    output_p[2] = rs.course_name
                    output_p[3] = rs.博士

            if max_m < rs.碩士:
                max_m = rs.碩士
                total_m = totalall
                output_m[0] = rs.課程代碼
                output_m[1] = rs.course_id
                output_m[2] = rs.course_name
                output_m[3] = rs.碩士
            elif max_m == rs.碩士:
                if total_m > totalall:
                    output_m[0] = rs.課程代碼
                    output_m[1] = rs.course_id
                    output_m[2] = rs.course_name
                    output_m[3] = rs.碩士

            if max_b < rs.學士:
                max_b = rs.學士
                total_b = totalall
                output_b[0] = rs.課程代碼
                output_b[1] = rs.course_id
                output_b[2] = rs.course_name
                output_b[3] = rs.學士
            elif max_b == rs.學士:
                if total_b > totalall:
                    output_b[0] = rs.課程代碼
                    output_b[1] = rs.course_id
                    output_b[2] = rs.course_name
                    output_b[3] = rs.學士

            if max_a < rs.副學士:
                max_a = rs.副學士
                total_a = totalall
                output_a[0] = rs.課程代碼
                output_a[1] = rs.course_id
                output_a[2] = rs.course_name
                output_a[3] = rs.副學士
            elif max_a == rs.副學士:
                if total_a > totalall:
                    output_a[0] = rs.課程代碼
                    output_a[1] = rs.course_id
                    output_a[2] = rs.course_name
                    output_a[3] = rs.副學士

            if max_hs < rs.高中:
                max_hs = rs.高中
                total_hs = totalall
                output_hs[0] = rs.課程代碼
                output_hs[1] = rs.course_id
                output_hs[2] = rs.course_name
                output_hs[3] = rs.高中
            elif max_hs == rs.高中:
                if total_hs > totalall:
                    output_hs[0] = rs.課程代碼
                    output_hs[1] = rs.course_id
                    output_hs[2] = rs.course_name
                    output_hs[3] = rs.高中

            if max_jhs < rs.國中:
                max_jhs = rs.國中
                total_jhs = totalall
                output_jhs[0] = rs.課程代碼
                output_jhs[1] = rs.course_id
                output_jhs[2] = rs.course_name
                output_jhs[3] = rs.國中
            elif max_jhs == rs.國中:
                if total_jhs > totalall:
                    output_jhs[0] = rs.課程代碼
                    output_jhs[1] = rs.course_id
                    output_jhs[2] = rs.course_name
                    output_jhs[3] = rs.國中

            if max_el < rs.國小:
                max_el = rs.國小
                total_el = totalall
                output_el[0] = rs.課程代碼
                output_el[1] = rs.course_id
                output_el[2] = rs.course_name
                output_el[3] = rs.國小
            elif max_el == rs.國小:
                if total_el > totalall:
                    output_el[0] = rs.課程代碼
                    output_el[1] = rs.course_id
                    output_el[2] = rs.course_name
                    output_el[3] = rs.國小

        to_render['output_p'] = output_p
        to_render['output_m'] = output_m
        to_render['output_b'] = output_b
        to_render['output_a'] = output_a
        to_render['output_hs'] = output_hs
        to_render['output_jhs'] = output_jhs
        to_render['output_el'] = output_el

    return to_render


def ExistorNot(cid, course_data):
    exist = None
    for cd in course_data:
        if cd.course_id == cid:
            exist = [cd.課程代碼, cd.course_id, cd.course_name]
            break

    return exist
