# -*- coding: utf-8 -*-
from servery import Server, CGIHandler

httpd = Server('127.0.0.1', 8000, CGIHandler)
httpd.serve_forever()