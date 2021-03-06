from xbmc import executebuiltin, Monitor
from resources.lib.server import create_server
from resources.lib.wsgi_app import *
from resources.lib.utils import notify, clear_session, RUNSCRIPT

executebuiltin(RUNSCRIPT)
monitor = Monitor()

httpd = create_server(app, LOCALHOST, port=port)
httpd.timeout = 0.1
starting = True

while not monitor.abortRequested():
  httpd.handle_request()
  if starting:
    notify(translate(32006) % port)
    starting = False

httpd.socket.close()
clear_session()
log(translate(32003))