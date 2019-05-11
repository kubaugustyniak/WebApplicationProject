
from app import app, db
from app.models import User
from flask_migrate import Migrate


app.app_context().push()
migrate=Migrate(app,db)

if __name__ == '__main__':
    app.run('127.0.0.1',8080,True)



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
