# -*- coding: utf-8 -*-
from servery import Server, CGIHandler

httpd = Server('', 5000, CGIHandler)
httpd.serve_forever()