from . import db
import datetime

class ChatMsgs(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    sender_email = db.Column(db.String(100))
    receiver_email  = db.Column(db.String(100))
    created_date = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    msg = db.Column(db.String(1000))

    def __repr__(self):
        return '<Sent by %r, from: %r, msg: %r>' % self.sender_email, self.receiver_email, self.msg
