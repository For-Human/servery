# -*- coding: utf-8 -*-
from servery import Server, StaticHandler

httpd = Server('127.0.0.1', 8000, StaticHandler)
httpd.serve_forever()