from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

from app import app


http_server = WSGIServer(('',  app.config['AUTH_PORT']), app)
http_server.serve_forever()
