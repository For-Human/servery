# -*- coding: utf-8 -*-
import re
import datetime
from collections import defaultdict

class Handler(object):
    """Handler is a base class.
    
    :param server: web server instance
    :param client_socket: client socket
    :param client_address: client address
    """

    routes = []
    
    def __init__(self, server, client_socket, client_address):
        self.server = server
        self.client_socket = client_socket
        self.client_address = client_address
        self.handle()
        
    def handle(self):
        result = None
        print '[{time}] {host}:{port}'.format(
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            host = self.client_address[0],
            port = self.client_address[1],
        )
        
        try:
            request = self.client_socket.recv(1024)
            request_dict, query_dict, form_dict = self.parse_request(request)
            for method, path, func_name in self.routes:
                if method == request_dict['REQUEST_METHOD']:
                    m = re.match('^' + path + '$', request_dict['REQUEST_PATH'])
                    if m:
                        func = getattr(self, func_name)
                        result = func(request_dict, query_dict, form_dict)
                        break
        except:
            pass
        
        if result is None:
            result = self.notfound()

        self.client_socket.sendall(result)
        self.client_socket.close()
    
    def parse_request(self, request):
        request_dict = {}
        query_dict   = defaultdict(list)
        form_dict    = defaultdict(list)
        
        request_lines = request.splitlines()
        if not request_lines:
            return request_dict, query_dict, form_dict
            
        # deal with::
        #
        # REQUEST_METHOD, REQUEST_PATH, REQUEST_VERSION
        # QUERY_STRING
        tmp = request_lines[0].split(' ')
        tmq = tmp[1].split('?')
        request_dict['REQUEST_METHOD'] = tmp[0]
        request_dict['REQUEST_PATH']   = tmq[0]
        
        if len(tmp) == 3:
            request_dict['REQUEST_VERSION'] = tmp[2]
            
        if len(tmq) == 2:
            for _ in tmq[1].split('&'):
                kv = _.split('=')
                query_dict[kv[0]].append(kv[1])
        
        if len(request_lines) == 1:
            return request_dict, query_dict, form_dict
        
        # deal with::
        #
        # HEADERS
        index = 1
        for _ in request_lines[1:]:
            index += 1
            kv = _.split(':')
            if len(kv) == 1:
                break
            request_dict[kv[0]] = ':'.join(kv[1:])
        
        # deal with::
        #
        # FORM_DATA
        if len(request_lines) > index:
            for _ in request_lines[index].split('&'):
                kv = _.split('=')
                form_dict[kv[0]].append(kv[1])
                    
        return request_dict, query_dict, form_dict
        
    def set_response(self, code):
        response = {
            100: 'Continue',
            101: 'Switching Protocols',
            102: 'Processing',
        
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            207: 'Multi Status',
            226: 'IM Used',
        
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            307: 'Temporary Redirect',
        
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Request Entity Too Large',
            414: 'Request URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Requested Range Not Satisfiable',
            417: 'Expectation Failed',
            418: 'I\'m a teapot',
            422: 'Unprocessable Entity',
            423: 'Locked',
            424: 'Failed Dependency',
            426: 'Upgrade Required',
        
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported',
            507: 'Insufficient Storage',
            510: 'Not Extended',
        }
        
        return 'HTTP/1.1 {code}{status}\r\n'.format(
            code   = code, 
            status = response[code],
        )  
        
    def set_header(self, key, value):
        return '{key}: {value}\r\n'.format(
            key   = key,
            value = value,
        )
        
    def set_body(self, body):
        return '\r\n{body}'.format(
            body = body,
        )
        
    def notfound(self):
        html = ''
        html += self.set_response(404)
        html += self.set_header('Content-Type', 'text/html')
        html += self.set_body('<h1>404 Not Found</h1>')
        return html