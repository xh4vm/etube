# from gevent import monkey
# monkey.patch_all()
# from gevent.pywsgi import WSGIServer

from api.app import create_app
from core.config import CONFIG

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG.APP.AUTH_APP_PORT)
    # http_server = WSGIServer(('0.0.0.0', CONFIG.APP.AUTH_APP_PORT), app)
    # http_server.serve_forever()
