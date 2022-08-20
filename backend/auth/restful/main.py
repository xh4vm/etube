from gevent import monkey
monkey.patch_all()

from api.app import create_app

app = create_app()
