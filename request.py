from sqlmodel import Session, select
from db import engine
from models import Guest, Administrator, RoomModel, Booking, PaymentModel, Service  # ИЗМЕНЕНО
from datetime import date

# Получить всех гостей
def get_all_guests():
    with Session(engine) as session:
        guests = session.exec(select(Guest)).all()
        return guests

# Получить все бронирования конкретного гостя
def get_bookings_by_guest(guest_id: int):
    with Session(engine) as session:
        bookings = session.exec(
            select(Booking).where(Booking.guest_id == guest_id)
        ).all()
        return bookings

# Получить доступные комнаты 
def get_available_rooms():
    with Session(engine) as session:
        rooms = session.exec(select(RoomModel).where(RoomModel.is_active == True)).all()  
        return rooms

# Создать новое бронирование
def create_booking(guest_id: int, room_id: int, admin_id: int, check_in: date, check_out: date, guests_count: int, total_price):
    from models import Booking
    from decimal import Decimal
    with Session(engine) as session:
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            admin_id=admin_id,
            check_in_date=check_in,
            check_out_date=check_out,
            status="confirmed",
            total_price=Decimal(total_price),
            guests_count=guests_count
        )
        session.add(booking)
        session.commit()
        session.refresh(booking)
        return booking

# Получить платежи по бронированию
def get_payments_by_booking(booking_id: int):
    with Session(engine) as session:
        payments = session.exec(
            select(PaymentModel).where(PaymentModel.booking_id == booking_id) 
        ).all()
        return payments

# Получить услуги гостя
def get_services_by_guest(guest_id: int):
    with Session(engine) as session:
        services = session.exec(
            select(Service).where(Service.guest_id == guest_id)
        ).all()
        return services

# Пример бронирования с деталями гостя и комнаты
def get_booking_details():
    with Session(engine) as session:
        bookings = session.exec(
            select(Booking)
        ).all()
        details = []
        for b in bookings:
            details.append({
                "booking_id": b.id,
                "guest": f"{b.guest.first_name} {b.guest.last_name}" if b.guest else None,
                "room_number": b.room.number if b.room else None,
                "status": b.status,
                "total_price": b.total_price
            })
        return details