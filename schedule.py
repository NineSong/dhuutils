#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from student import Student

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(u'用法：' + sys.argv[0] + u' 学号 教务密码 学期')

    student = Student(sys.argv[1], sys.argv[2])
    print(u'学生姓名：' + student.name)
    schedule = student.schedule(sys.argv[3])

    if schedule:
        filename = 'schedule_' + sys.argv[3] + '.html'

        with open(filename, 'w') as file:
            file.write(schedule)

        print(u'课程表已保存到' + filename)
    else:
        print(u'该学期不存在')
