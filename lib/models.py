from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from connect import session

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    auditions = relationship("Audition", back_populates="role")

    @property
    def actors(self):
        actors = [audition.actor for audition in self.auditions]
        return actors

    @property
    def locations(self):
        locations = [audition.location for audition in self.auditions]
        return locations

    def lead(self):
        auditions = self.auditions.sort(key=lambda a: a.id)
        if not auditions:
            return "no actor has been hired for this role"
        else:
            return auditions[0]

    def understudy(self):
        auditions = self.auditions.sort(key=lambda a: a.id)
        if not auditions:
            return "no actor has been hired for understudy for this rol"
        else:
            return auditions[1]


class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Boolean)
    hired = Column(Integer)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def call_back(self):
        self.hired = True
        session.commit()