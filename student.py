# -*- coding: utf-8 -*-

import requests
import pyquery

def courseName(course_id):
    pq = pyquery.PyQuery(
        'http://jwdep.dhu.edu.cn/dhu/ftp/' + course_id[:2] + '/' + course_id + 'DG.htm'
    )
    title = pq('title').html()

    try:
        return title.encode('iso-8859-1').decode('gb2312')
    # Some pages declare that they use gb2312, but in reality they use unicode.
    except UnicodeEncodeError:
        return title

class Student(object):
    def __init__(self, student_id, password):
        self._session = requests.Session()
        response = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/login_wz.jsp',
            params={'userName': student_id, 'userPwd': password},
            allow_redirects=False
        )

        if 'Location' not in response.headers:
            exit(u'用户名或密码错误')

        response = self._session.get('http://jwdep.dhu.edu.cn/dhu/student/modifyselfinfo.jsp')
        pq = pyquery.PyQuery(response.text)
        self.name = pq('table')('td').eq(3).html()

    def printCourseInfo(self, course_number):
        response = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/student/selectcourse/selectcourse2.jsp',
            params={'courseNo': course_number}
        )
        pq = pyquery.PyQuery(response.text)

        if len(pq('tr')) == 0:
            exit(u'选课未开放或课程不存在')

        course_id = pq('tr').eq(1)('td').eq(1).html()
        name = courseName(course_id)
        print(u'课程名称：' + name)
        print(u'课程编号：' + course_id)
        response = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/commonquery/coursetimetableinfo.jsp',
            params={'courseId': course_id}
        )
        pq = pyquery.PyQuery(response.text)

        for i in pq('table').children('tr').items():
            if course_number == i('td').html():
                print(u'任课教师：' + i('td').eq(6)('a').html())
                break

    def getCourses(self):
        self.course = [{}]
        response = self._session.get('http://jwdep.dhu.edu.cn/dhu/student/selectcourse/seeselectedcourse.jsp')
        pq = pyquery.PyQuery(response.text)
        table = pq('table').eq(2)

        for i, tr in enumerate(table.children('tr')):
            if i:
                td = pq(tr)('td')
                self.course.append({
                    'id': td.html(),
                    'name': td.eq(1)('a').html(),
                    'class_id': td.eq(4).html(),
                    'teacher': td.eq(7)('a').html()
                })

    def selectCourse(self, course_number):
        headers = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/servlet/com.collegesoft.eduadmin.tables.selectcourse.SelectCourseController',
            params={
                'doWhat': 'selectcourse',
                'courseName': '',
                'courseNo': course_number
            },
            allow_redirects=False
        ).headers

        return 'Location' in headers and headers['Location'][-8:] == 'Status=2'

    def deleteCourse(self, course):
        response = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/servlet/com.collegesoft.eduadmin.tables.selectcourse.SelectCourseController',
            params={'classNo': course['class_id'], 'courseId': course['id'], 'doWhat': 'deletematriculatedcourse'}
        )
        pq = pyquery.PyQuery(response.text)
        return len(pq('table').eq(2).children('tr')) != len(self.course)

    def scoreReport(self, term):
        response = self._session.get(
            'http://jwdep.dhu.edu.cn/dhu/admin/score/classscorelist.jsp',
            params={'yearTerm': term},
            allow_redirects=False
        )

        if 'Location' in response.headers:
            return ''

        pq = pyquery.PyQuery(response.text)

        if len(pq('table')):
            return '<meta charset="utf-8">' + pq('div').eq(1).outerHtml() + pq('table').eq(1).outerHtml()

        return ''

    def schedule(self, term):
        response = self._session.post(
            'http://jwdep.dhu.edu.cn/dhu/student/studentcoursetable.jsp',
            data={'yt': term},
        )
        pq = pyquery.PyQuery(response.text)
        terms = []

        for i in pq('option'):
            terms.append(pq(i).html())

        if term in terms:
            return '<meta charset="utf-8">' + pq('div').eq(1).outerHtml() + pq('table').eq(1).outerHtml()
        else:
            return ''
