from typing import Optional, List
from decimal import Decimal
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Numeric, Text, String

class Guest(SQLModel, table=True):
    __tablename__ = "guest"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    passport_data: Optional[str] = Field(default=None, max_length=255)

    bookings: List["Booking"] = Relationship(back_populates="guest")
    services: List["Service"] = Relationship(back_populates="guest")

class Administrator(SQLModel, table=True):
    __tablename__ = "administrator"
    id: Optional[int] = Field(default=None, primary_key=True)
    role: Optional[str] = None
    username: str = Field(sa_column=Column(String(50), unique=True))
    password_hash: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    bookings: List["Booking"] = Relationship(back_populates="admin")

class RoomModel(SQLModel, table=True):  # ИЗМЕНЕНО: Room -> RoomModel
    __tablename__ = "room"
    id: Optional[int] = Field(default=None, primary_key=True)
    number: str = Field(sa_column=Column(String(10), unique=True))
    type: Optional[str] = None
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    price_per_night: Decimal = Field(sa_column=Column(Numeric(10,2)))
    max_guests: Optional[int] = None
    is_active: bool = Field(default=True)

    bookings: List["Booking"] = Relationship(back_populates="room")

class Booking(SQLModel, table=True):
    __tablename__ = "booking"
    id: Optional[int] = Field(default=None, primary_key=True)
    guest_id: Optional[int] = Field(default=None, foreign_key="guest.id")
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
    admin_id: Optional[int] = Field(default=None, foreign_key="administrator.id")
    check_in_date: date
    check_out_date: date
    status: Optional[str] = None
    total_price: Decimal = Field(sa_column=Column(Numeric(10,2)))
    guests_count: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    guest: Optional[Guest] = Relationship(back_populates="bookings")
    room: Optional[RoomModel] = Relationship(back_populates="bookings")  # ИЗМЕНЕНО
    admin: Optional[Administrator] = Relationship(back_populates="bookings")
    payments: List["PaymentModel"] = Relationship(back_populates="booking")  # ИЗМЕНЕНО
    services: List["Service"] = Relationship(back_populates="booking")

class PaymentModel(SQLModel, table=True):  # ИЗМЕНЕНО: Payment -> PaymentModel
    __tablename__ = "payment"
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: Optional[int] = Field(default=None, foreign_key="booking.id")
    amount: Decimal = Field(sa_column=Column(Numeric(10,2)))
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = Field(default=None, sa_column=Column(String(100), unique=True))
    paid_at: Optional[datetime] = None

    booking: Optional[Booking] = Relationship(back_populates="payments")

class Service(SQLModel, table=True):
    __tablename__ = "services"
    id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = None
    employee: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: Optional[str] = None
    service_time: Optional[datetime] = None
    guest_id: Optional[int] = Field(default=None, foreign_key="guest.id")
    booking_id: Optional[int] = Field(default=None, foreign_key="booking.id")

    guest: Optional[Guest] = Relationship(back_populates="services")
    booking: Optional[Booking] = Relationship(back_populates="services")