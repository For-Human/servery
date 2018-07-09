# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import socket
import copy
from .statichandler import StaticHandler

class CGIHandler(StaticHandler):
    """CGIHandler is a subclass of StaticHandler."""
    
    routes = [
        ('GET', '/static/.*', 'static'),
        ('POST', '/cgi/.*', 'cgi'),
    ]
    
    def cgi(self, request_dict, query_dict, form_dict):
        tmp = ''
        for key, value in form_dict.iteritems():
            for _ in value:
                tmp += key + '=' + _ + '&'
            
        environ = copy.deepcopy(os.environ)
        environ['SERVER_SOFTWARE']   = 'CGI/1.1'
        environ['SERVER_NAME']       = socket.getfqdn(self.server.socket.getsockname()[0])
        environ['SERVER_PORT']       = str(self.server.socket.getsockname()[1])
        environ['REMOTE_ADDR']       = self.client_address[0]
        environ['SCRIPT_NAME']       = request_dict['REQUEST_PATH'].split('/')[-1]
        environ['REQUEST_METHOD']    = 'POST'
        environ['PATH_INFO']         = request_dict['REQUEST_PATH']
        environ['QUERY_STRING']      = tmp[:-1]
        environ['CONTENT_TYPE']      = request_dict.get('Content-Type', '')
        environ['CONTENT_LENGTH']    = request_dict.get('Content-Length', '')
        environ['HTTP_USER_AGENT']   = request_dict.get('User-Agent', '')
        environ['HTTP_COOKIE']       = request_dict.get('Cookie', '')
        
        commandline = [
            sys.executable,
            '-u',
           os.path.join(os.getcwd(), *request_dict['REQUEST_PATH'].split('/')),
        ]
        p = subprocess.Popen(
            commandline,
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            env    = environ,
        )
        stdout, stderr = p.communicate()
        p.stderr.close()
        p.stdout.close()
        
        html = ''
        html += self.set_response(200)
        html += self.set_header('Content-Type', 'text/html')
        html += self.set_body(stdout)
        return html