from sqlalchemy import String, Integer, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(1000), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)


class Meal(Base):
    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    meat: Mapped[str] = mapped_column(String(15), nullable=True)
    vegetarian: Mapped[bool] = mapped_column(Boolean)
    active: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        CheckConstraint(
            "(meat IS NOT NULL) OR (vegetarian = 1)",
            name="check_meat_or_vegetarian_true"
        ),
    )


class UserPreferences(Base):
    __tablename__ = "preferences"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    vegetarian: Mapped[bool] = mapped_column(default=False)
    no_beef: Mapped[bool] = mapped_column(default=False)
    no_chicken: Mapped[bool] = mapped_column(default=False)
    no_pork: Mapped[bool] = mapped_column(default=False)


class Favorite(Base):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), nullable=False)

    user = db.relationship("User", backref="favorites")
    meal = db.relationship("Meal", backref="favorites")


dummy_records = [
    Meal(name="Krupicová kaše", vegetarian=True, active=True),
    Meal(name="Kuřecí kousky ve smetanové omáčce", meat="Kuřecí", vegetarian=False, active=True),
    Meal(name="Kuřecí kung-pao", meat="Kuřecí", vegetarian=False, active=True),
    Meal(name="Trhané vepřové", meat="Vepřové", vegetarian=False, active=True),
    Meal(name="Buchtičky se šodó", vegetarian=True, active=True),
    Meal(name="Koprová omáčka", meat="Hovězí", vegetarian=False, active=True),
    Meal(name="Rajská omáčka", meat="Hovězí", vegetarian=False, active=True),
    Meal(name="Nudle s mákem", vegetarian=True, active=True),
    Meal(name="Kuřecí na smetaně", meat="Kuřecí", vegetarian=False, active=False),
    Meal(name="Rizoto", meat="Kuřecí", vegetarian=False, active=True),
    Meal(name="Smažený sýr", vegetarian=True, active=True),
    Meal(name="Ovocné knedlíky", vegetarian=True, active=True),
    Meal(name="Pečené kuře", meat="Kuřecí", vegetarian=False, active=False),
    Meal(name="Vepřové na houbách", meat="Vepřové", vegetarian=False, active=False),
    Meal(name="Svíčková na smetaně", meat="Hovězí", vegetarian=False, active=True)
]
