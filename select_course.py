#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pyquery
import time
import sys

# The course names locate in "http://jw.dhu.edu.cn/dhu/ftp/**/******DG.htm".
# "******" is the course id and "**" is the first two digits of course id.
def course_name(course_id):
    pq = pyquery.PyQuery(
        url='http://jw.dhu.edu.cn/dhu/ftp/' + course_id[:2] + '/' + course_id + 'DG.htm'
    )
    title = pq('title').html()

    try:
        return title.encode('iso-8859-1').decode('gb2312')
    # Some pages declare that they use gb2312, but in reality they use unicode.
    except UnicodeEncodeError:
        return title

class Student(object):
    def __init__(self, student_id, password):
        self._id = student_id
        self._password = password
        self._session = requests.Session()
        response = self._session.get(
            'http://jw.dhu.edu.cn/dhu/login_wz.jsp',
            params={'userName': student_id, 'userPwd': password},
            allow_redirects=False
        )

        if 'Location' not in response.headers:
            exit(u'用户名或密码错误')

        response = self._session.get('http://jw.dhu.edu.cn/dhu/student/modifyselfinfo.jsp')
        pq = pyquery.PyQuery(response.text)
        name = pq('table')('td').eq(3).html()

        if name:
            print(u'学生姓名：' + name)
        else:
            print(u'学生姓名：未知')

        self._get_course_info(sys.argv[3])

    def _get_course_info(self, course_number):
        response = self._session.get(
            'http://jw.dhu.edu.cn/dhu/student/selectcourse/selectcourse2.jsp',
            params={'courseNo': course_number}
        )
        pq = pyquery.PyQuery(response.text)

        if len(pq('tr')) == 0:
            exit(u'选课未开放')

        course_id = pq('tr').eq(1)('td').eq(1).html()

        if course_id is None:
            exit(u'课程不存在')

        name = course_name(course_id)
        print(u'课程名称：' + name)
        print(u'课程编号：' + course_id)

        response = self._session.get(
            'http://jw.dhu.edu.cn/dhu/commonquery/coursetimetableinfo.jsp',
            params={'courseId': course_id, 'courseName': ''}
        )
        pq = pyquery.PyQuery(response.text)

        for i in pq('table').children('tr').items():
            if course_number == i('td').html():
                print(u'任课教师：' + i('td').eq(6)('a').html())
                break

    def select_course(self, course_number):
        headers = self._session.get(
            'http://jw.dhu.edu.cn/dhu/servlet/com.collegesoft.eduadmin.tables.selectcourse.SelectCourseController',
            params={
                'doWhat': 'selectcourse',
                'courseName': '',
                'courseNo': course_number
            },
            allow_redirects=False
        ).headers

        return 'Location' in headers and headers['Location'][-8:] == 'Status=2'


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit()

    student = Student(sys.argv[1], sys.argv[2])

    while 1:
        try:
            if student.select_course(sys.argv[3]):
                exit(u'选课成功')
            else:
                print(u'选课失败')
                time.sleep(0.8)
        except requests.exceptions.RequestException:
            print(u'网络连接失败')
            time.sleep(3)
