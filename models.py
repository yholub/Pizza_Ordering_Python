# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, Numeric, Time, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import BIT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata


class Address(Base):
    __tablename__ = 'Addresses'

    Id = Column(BigInteger, primary_key=True)
    City = Column(Unicode, nullable=False)
    District = Column(Unicode, nullable=False)
    Street = Column(Unicode, nullable=False)
    HouseNumber = Column(Unicode, nullable=False)
    Lng = Column(Float(53), nullable=False)
    Lat = Column(Float(53), nullable=False)


class CapacityPlan(Base):
    __tablename__ = 'CapacityPlans'

    Id = Column(BigInteger, primary_key=True)
    PizzaHouseId = Column(ForeignKey('PizzaHouses.Id'), nullable=False, index=True)
    FromTime = Column(DateTime, nullable=False)
    ToTime = Column(DateTime, nullable=False)
    TimeForOnePizza = Column(Time, nullable=False)
    CountOfPizza = Column(Integer, nullable=False)

    PizzaHouse = relationship('PizzaHouse')


class FixPizza(Base):
    __tablename__ = 'FixPizzas'

    Id = Column(BigInteger, primary_key=True)
    Name = Column(Unicode, nullable=False)
    Price = Column(Numeric(18, 2), nullable=False)


class IngredientAmount(Base):
    __tablename__ = 'IngredientAmounts'

    Id = Column(BigInteger, primary_key=True)
    IngredientId = Column(ForeignKey('Ingredients.Id'), nullable=False, index=True)
    PizzaHouseId = Column(ForeignKey('PizzaHouses.Id'), nullable=False, index=True)
    Quantity = Column(Integer, nullable=False)

    Ingredient = relationship('Ingredient')
    PizzaHouse = relationship('PizzaHouse')


class IngredientItem(Base):
    __tablename__ = 'IngredientItems'

    Id = Column(BigInteger, primary_key=True)
    IngredientId = Column(ForeignKey('Ingredients.Id'), nullable=False, index=True)
    Quantity = Column(Integer, nullable=False)
    FixPizza_Id = Column(ForeignKey('FixPizzas.Id'), index=True)
    ModifiedPizza_Id = Column(ForeignKey('ModifiedPizzas.Id'), index=True)
    SavedPizza_Id = Column(ForeignKey('SavedPizzas.Id'), index=True)

    FixPizza = relationship('FixPizza')
    Ingredient = relationship('Ingredient')
    ModifiedPizza = relationship('ModifiedPizza')
    SavedPizza = relationship('SavedPizza')


class Ingredient(Base):
    __tablename__ = 'Ingredients'

    Id = Column(BigInteger, primary_key=True)
    Name = Column(Unicode)
    Price = Column(Numeric(18, 2), nullable=False)
    Weight = Column(Float(53), nullable=False)


class ModifiedPizza(Base):
    __tablename__ = 'ModifiedPizzas'

    Id = Column(BigInteger, primary_key=True)
    FixPizzaId = Column(ForeignKey('FixPizzas.Id'), nullable=False, index=True)

    FixPizza = relationship('FixPizza')


class OrderItem(Base):
    __tablename__ = 'OrderItems'

    Id = Column(BigInteger, primary_key=True)
    PizzaId = Column(BigInteger, nullable=False)
    IsModified = Column(BIT, nullable=False)
    StartTime = Column(DateTime, nullable=False)
    EndTime = Column(DateTime, nullable=False)
    OrderId = Column(ForeignKey('Orders.Id'), nullable=False, index=True)
    Price = Column(Numeric(18, 2), nullable=False)

    Order = relationship('Order')


class Order(Base):
    __tablename__ = 'Orders'

    Id = Column(BigInteger, primary_key=True)
    Price = Column(Numeric(18, 2), nullable=False)
    UserId = Column(ForeignKey('Users.Id'), index=True)
    PizzaHouseId = Column(ForeignKey('PizzaHouses.Id'), nullable=False, index=True)
    Status = Column(Integer, nullable=False)
    TimeToTake = Column(DateTime, nullable=False)

    PizzaHouse = relationship('PizzaHouse')
    User = relationship('User')


class PizzaHouse(Base):
    __tablename__ = 'PizzaHouses'

    Id = Column(BigInteger, primary_key=True)
    AddressId = Column(ForeignKey('Addresses.Id'), nullable=False, index=True)
    OpenTime = Column(Time, nullable=False)
    CloseTime = Column(Time, nullable=False)
    ModeratorId = Column(ForeignKey('Users.Id'), nullable=False, index=True)
    Capacity = Column(Integer, nullable=False)

    Address = relationship('Address')
    User = relationship('User')


class Role(Base):
    __tablename__ = 'Roles'

    Id = Column(BigInteger, primary_key=True)
    Name = Column(Unicode)


class SavedPizza(Base):
    __tablename__ = 'SavedPizzas'

    Id = Column(BigInteger, primary_key=True)
    UserId = Column(ForeignKey('Users.Id'), nullable=False, index=True)
    Name = Column(Unicode)
    FixPizzaId = Column(ForeignKey('FixPizzas.Id'), nullable=False, index=True)

    FixPizza = relationship('FixPizza')
    User = relationship('User')


class UserBonu(Base):
    __tablename__ = 'UserBonus'

    Id = Column(BigInteger, primary_key=True)
    UserId = Column(ForeignKey('Users.Id'), nullable=False, index=True)
    Count = Column(Integer, nullable=False)
    Percent = Column(Integer, nullable=False)

    User = relationship('User')


class UserClaim(Base):
    __tablename__ = 'UserClaims'

    Id = Column(Integer, primary_key=True)
    UserId = Column(ForeignKey('Users.Id'), nullable=False, index=True)
    ClaimType = Column(Unicode)
    ClaimValue = Column(Unicode)

    User = relationship('User')


class UserLogin(Base):
    __tablename__ = 'UserLogins'

    ProviderKey = Column(Unicode(128), primary_key=True, nullable=False)
    LoginProvider = Column(Unicode(128), primary_key=True, nullable=False)
    UserId = Column(ForeignKey('Users.Id'), primary_key=True, nullable=False, index=True)

    User = relationship('User')


class UserRole(Base):
    __tablename__ = 'UserRoles'

    UserId = Column(ForeignKey('Users.Id'), primary_key=True, nullable=False, index=True)
    RoleId = Column(BigInteger, primary_key=True, nullable=False)
    CustomRole_Id = Column(ForeignKey('Roles.Id'), index=True)

    Role = relationship('Role')
    User = relationship('User')


class User(Base):
    __tablename__ = 'Users'

    Id = Column(BigInteger, primary_key=True)
    Name = Column(Unicode)
    Photo = Column(Unicode)
    UserName = Column(Unicode)
    Email = Column(Unicode)
    EmailConfirmed = Column(BIT, nullable=False)
    PasswordHash = Column(Unicode)
    SecurityStamp = Column(Unicode)
    PhoneNumber = Column(Unicode)
    PhoneNumberConfirmed = Column(BIT, nullable=False)
    TwoFactorEnabled = Column(BIT, nullable=False)
    LockoutEndDateUtc = Column(DateTime)
    LockoutEnabled = Column(BIT, nullable=False)
    AccessFailedCount = Column(Integer, nullable=False)


class MigrationHistory(Base):
    __tablename__ = '__MigrationHistory'

    MigrationId = Column(Unicode(150), primary_key=True, nullable=False)
    ContextKey = Column(Unicode(300), primary_key=True, nullable=False)
    Model = Column(LargeBinary, nullable=False)
    ProductVersion = Column(Unicode(32), nullable=False)

url = 'mssql+pyodbc://(localdb)\\v11.0/Pizza_Ordering?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes'

engine = create_engine(url)
engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
def getSession() :
    return Session()