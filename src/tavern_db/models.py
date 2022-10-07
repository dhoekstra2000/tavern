from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base, db_session

group_permission_table = Table(
    "group_permission_association",
    Base.metadata,
    Column("group_id", ForeignKey("usergroup.id")),
    Column("permission_id", ForeignKey("permission.id")),
)


class User(Base):
    username = Column(String(32))
    password = Column(String)
    group_id = Column(ForeignKey("usergroup.id"))
    group = relationship("UserGroup", back_populates="users")

    def has_permission(self, name):
        if self.group.superuser:
            return True
        perm = Permission.query.filter(Permission.name == name).first()
        if not perm or not self.group.permissions:
            return False
        return True


class Permission(Base):
    name = Column(String)


class UserGroup(Base):
    name = Column(String)
    superuser = Column(Boolean)
    users = relationship("User", back_populates="group")
    permissions = relationship("Permission", secondary=group_permission_table)

    def grant_permission(self, name):
        perm = Permission.query.filter(Permission.name == name).first()
        if perm and perm in self.permissions:
            return
        if not perm:
            perm = Permission()
            perm.name = name
            db_session.add(perm)
            db_session.commit()
        self.permissions.append(perm)

    def revoke_permission(self, name):
        perm = Permission.query.filter(Permission.name == name).first()
        if not perm or not perm in self.permissions:
            return
        self.permissions.remove(perm)
