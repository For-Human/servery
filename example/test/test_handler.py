# -*- coding: utf-8 -*-
from servery import Server, Handler

class MyHandler(Handler):
    
    routes = [
        ('GET', '/', 'index'),
        ('POST', '/summary', 'summary'),
    ]
    
    def index(self, request_dict, query_dict, form_dict):
        html = ''
        html += self.set_response(200)
        html += self.set_header('Content-Type', 'text/html')
        html += self.set_body('''
            <form action="/summary" method="POST">
                Name: <input type="text" name="name"><br>
                Age:  <input type="text" name="age"><br>
                <input type="submit">
            </form>
        ''')
        return html
        
    def summary(self, request_dict, query_dict, form_dict):
        name = form_dict['name'][0]
        age  = form_dict['age'][0]
        html = ''
        html += self.set_response(200)
        html += self.set_header('Content-Type', 'text/html')
        html += self.set_body('<p>My name is {name}. I am {age}.<p>'.format(name=name, age=age))
        return html
        
httpd = Server('', 5000, MyHandler)
httpd.serve_forever()