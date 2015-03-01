#!/usr/bin/python
import os


# When running locally can safely ignore this. i.e. run 'python wsgi.py' to test outside Openshift.
try:
    virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    execfile(virtualenv, dict(__file__=virtualenv))
except KeyError, IOError:
    pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

from cgi import parse_qs

def application(environ, start_response):

    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/capbin':
        from wxjson import binary_wxjson
        # Download as JSON and forward as binary 'arraybuffer'
        # However GeoTIFFfloat or NetCDF3 might be more efficient formats
        params = parse_qs(environ['QUERY_STRING'])
        response_body = binary_wxjson(r.text)
        ctype = 'text/plain'
    elif environ['PATH_INFO'] == '/cappng':
        from wxjson import pngB_wxjson, pngFloat_wxjson
        from testdata import ubyte_small, uint_small, float_small
        params = parse_qs(environ['QUERY_STRING'])
        response_body = pngFloat_wxjson(float_small)
        ctype = 'image/png'
    else:
        ctype = 'text/html'
        response_body = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <title>A test</title>
</head>
<body>
<p>A test</p>
</body>
</html>'''

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body))),
                        ('Access-Control-Allow-Origin', '*')]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#

def static_application(environ, start_response):
    if environ['PATH_INFO'].startswith('/static/'):
        return static_app(environ, start_response)
    else:
        return application(environ, start_response)

MIME_TABLE = {'.txt': 'text/plain',
              '.html': 'text/html',
              '.css': 'text/css',
              '.js': 'application/javascript',
              }

def content_type(path):
    name, ext = os.path.splitext(path)

    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"

def static_app(environ, start_response):
    path = environ['PATH_INFO']
    path = path.replace('/static/', '../client/')
    if os.path.exists(path):
        h = open(path, 'rb')
        content = h.read()
        h.close()

        headers = [('content-type', content_type(path))]
        start_response('200 OK', headers)
        return [content]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, static_application)
    print "Test server running at http://localhost:8051"
    httpd.serve_forever()
