import os
from app import create_app, db
from app.models import User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

if __name__ == '__main__':
    app.run('127.0.0.1',8080,True)



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
