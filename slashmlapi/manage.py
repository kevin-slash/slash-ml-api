from flask_script import Manager

from slashmlapi.test_request import application

manager = Manager(application)

@manager.command
def hello():
    print("hello")

if __name__ == "__main__":
    manager.run()