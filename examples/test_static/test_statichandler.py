# -*- coding: utf-8 -*-
from servery import Server, StaticHandler

httpd = Server('', 5000, StaticHandler)
httpd.serve_forever()