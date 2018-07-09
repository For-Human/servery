# servery

`servery` reconstructs the web server in python standard library, and big picture is showed below:

- `Server`: `BaseHTTPServer.HTTPServer`
- `Handler` `BaseHTTPServer.BaseHTTPRequestHandler`
- `StaticHandler`: `SimpleHTTPServer.SimpleHTTPRequestHandler`
- `CGIHandler`: `CGIHTTPServer.CGIHTTPRequestHandler`

## hello world

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
        
httpd = Server('127.0.0.1', 8000, MyHandler)
httpd.serve_forever()
```

## example

- [ex_handler](https://github.com/For-Human/servery/tree/master/example/ex_handler)
- [ex_staitc](https://github.com/For-Human/servery/tree/master/example/ex_static)
- [ex_cgi](https://github.com/For-Human/servery/tree/master/example/ex_cgi)