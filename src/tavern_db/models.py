from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
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
    superuser = Column(Boolean, default=False)
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


class Relation(Base):
    name = Column(String, nullable=False)
    short_name = Column(String(32))
    kvk_number = Column(String)

    address = Column(String, nullable=False)
    email = Column(String, nullable=False)

    account = Column(String)
    budget = Column(Integer)

    @hybrid_property
    def has_budget(self):
        return self.budget is not None

    @has_budget.setter
    def has_budget(self, value):
        self.budget = 0 if value else None


class BtwType(Base):
    name = Column(String(16))
    percentage = Column(Integer)


class SalesPrice(Base):
    date_from = Column(DateTime, default=datetime.utcnow)
    price = Column(Integer)
    btw_id = Column(ForeignKey("btwtype.id"))
    btw = relationship("BtwType")

    product_id = Column(ForeignKey("product.id"))


class ProductPosition(Base):
    amount = Column(Integer)
    value = Column(Integer)
    product_id = Column(ForeignKey("product.id"))


class Group(Base):
    name = Column(String)

    products = relationship("Product", back_populates="group")


class Product(Base):
    name = Column(String, nullable=False)
    tag = Column(String(32))
    group_id = Column(ForeignKey("group.id"))
    group = relationship("Group", back_populates="products")

    sales_prices = relationship(
        "SalesPrice", lazy="dynamic", order_by="desc(SalesPrice.date_from)"
    )
    product_positions = relationship(
        "ProductPosition", lazy="dynamic", order_by="desc(ProductPosition.date_updated)"
    )

    @hybrid_property
    def current_price(self):
        return self.sales_prices.filter(
            SalesPrice.date_from <= datetime.utcnow()
        ).first()

    @hybrid_property
    def current_position(self):
        return self.product_positions.first()

    @hybrid_property
    def amount(self):
        return self.current_position.amount

    @hybrid_property
    def value(self):
        return self.current_position.value
