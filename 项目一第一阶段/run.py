from app import create_app
from config.settings import config
import os

app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(
        host=app.config['FLASK_HOST'],
        port=app.config['FLASK_PORT'],
        debug=app.config['FLASK_DEBUG']
    )