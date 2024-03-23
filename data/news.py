from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from sqlalchemy_serializer import SerializerMixin

class Seeds(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'seeds'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    comment = sa.Column(sa.String, nullable=True)
    seed = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    user = orm.relationship('User')
