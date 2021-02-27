# models.py

from flask_login import UserMixin
from server import db
import typing

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100), default="customer")
    payment = db.Column(db.String(100), default="apple")

    phone = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(1000), nullable=True)
    name = db.Column(db.String(1000))
    
    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        '''
        Helper for __repr__
        '''
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        return self._repr(id=self.id,
                          user=self.name,
                          email=self.email,
                          phone=self.phone,
                          password=self.password,
                          role=self.role,
                          payment=self.payment)
        # return '<Name %r, email %r, phone %r, role %r, address %r, >' % self.name, self.email, self.phone, self.role, self.address
