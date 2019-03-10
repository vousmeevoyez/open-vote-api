"""
    Manage
    ___________________
    This is flask application entry
"""
import os
import unittest

from flask_migrate  import Migrate, MigrateCommand
from flask_script   import Manager, Shell

from app        import blueprint
from app.api    import create_app, socket
from app.api    import db

#import model here
from app.api        import models
from app.api.models import *

app = create_app(os.getenv("ENVIRONMENT") or 'dev')
app.register_blueprint(blueprint, url_prefix="/api/v1")

app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    """ function to start flask apps"""
    host = os.getenv("HOST") or '127.0.0.1'
    app.run(host=host)

@manager.command
def test():
    """ function to run unittest"""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def init():
    """ create init function here """
    admin = User(
        username="EVOTESUPERADMIN",
        email="kelvindsmn@gmail.com",
        role=0
    )
    admin.set_password("password")
    db.session.add(admin)
    db.session.commit()

def make_shell_context():
    """ create shell context here"""
    return {
        'app'      : app,
        'db'       : db,
        'User'     : User,
        'Election' : Election,
        'Candidate': Candidate,
    }

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
