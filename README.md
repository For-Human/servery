# servery

servery reconstructs the web server in python standard library.

- Server reconstructs BaseHTTPServer.HTTPServer
- Handler reconstructs BaseHTTPServer.BaseHTTPRequestHandler
- StaticHandler reconstructs SimpleHTTPServer.SimpleHTTPRequestHandler
- CGIHandler reconstructs CGIHTTPServer.CGIHTTPRequestHandler

## example

```python
from servery import Server, Handler

class MyHandler(Handler):
    
    routes = [
        ('GET', '/', 'index'),
    ]
    
    def index(self, request_dict, query_dict, form_dict):
        html = ''
        html += self.set_response(200)
        html += self.set_header('Content-Type', 'text/plain')
        html += self.set_body('Hello World!')
        return html
        
httpd = Server('', 5000, MyHandler)
httpd.serve_forever()
```

- [test](https://github.com/For-Human/servery/tree/master/example/test)
- [test_staitc](https://github.com/For-Human/servery/tree/master/example/test_static)
- [test_cgi](https://github.com/For-Human/servery/tree/master/example/test_cgi)