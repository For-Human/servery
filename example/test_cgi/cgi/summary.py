# -*- coding: utf-8 -*-
import cgi

form = cgi.FieldStorage()
name = form['name'].value
age  = form['age'].value
                          
print '<p>My name is {name}. I am {age}.<p>'.format(name=name, age=age)