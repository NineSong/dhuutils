#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from student import Student

if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(u'用法：' + sys.argv[0] + u' 学号 教务密码')

    student = Student(sys.argv[1], sys.argv[2])
    print(u'学生姓名：' + student.name + '\n')
    print(u'编号\t课程名称')
    student.getCourses()

    for i, course in enumerate(student.course):
        if i:
            print(str(i) + '\t' + course['name'])

    print(u'\n请输入您想删除的课程对应的编号:')
    print(u'（输入0退出）')

    while 1:
        try:
            num = int(input())

            if 0 < num < len(student.course):
                course = student.course[num]
                print(u'\n删除：' + course['name'] + ' ' + course['teacher'])
                print(u'是否确认？[y/n]')

                while 1:
                    reply = input()

                    if reply == 'y':
                        if student.deleteCourse(course):
                            print(u'\n删课成功')
                        else:
                            print(u'\n删课失败')

                        break
                    elif reply == 'n':
                        print(u'\n未删除课程')
                        break
                    else:
                        print(u'请输入y（确认）或n（放弃）')

                break
            elif num == 0:
                exit()
        except ValueError:
            pass

        print(u'输入错误，请重新输入')
