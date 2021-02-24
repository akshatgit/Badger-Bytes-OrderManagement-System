from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

socketio = SocketIO()

global db

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

class ChatMsgs(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    sender_email = db.Column(db.String(100))
    receiver_email  = db.Column(db.String(100))
    created_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    msg = db.Column(db.String(1000))

    def __repr__(self):
        return '<Sent by %r, from: %r, msg: %r>' % self.sender_email, self.receiver_email, self.msg

