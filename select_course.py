#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import sys

from student import Student

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(u'用法：' + sys.argv[0] + u' 学号 教务密码 选课序号')

    student = Student(sys.argv[1], sys.argv[2])
    print(u'学生姓名：' + student.name)
    student.printCourseInfo(sys.argv[3])

    while 1:
        try:
            if student.selectCourse(sys.argv[3]):
                exit(u'选课成功')
            else:
                print(u'选课失败')
                time.sleep(1)
        except requests.exceptions.RequestException:
            print(u'网络连接失败')
            time.sleep(3)
