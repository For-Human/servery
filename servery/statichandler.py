# -*- coding: utf-8 -*-
from .handler import Handler

class StaticHandler(Handler):
    """StaticHandler is a subclass of Handler."""
    
    routes = [
        ('GET', '/static/.*', 'static'),
    ]
    
    def static(self, request_dict, query_dict, form_dict):
        import os
        import mimetypes
        
        path = os.path.join(os.getcwd(), *request_dict['REQUEST_PATH'].split('/'))
        suffix = os.path.splitext(path)[1]
        
        html = ''
        html += self.set_response(200)
        html += self.set_header('Content-Type', mimetypes.types_map.get(suffix.lower(), ''))
        with open(path, 'rb') as f:
           html += self.set_body(f.read())
        return html