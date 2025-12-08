from sqlmodel import Session
from db import engine
from models import Guest, Administrator, RoomModel, Booking, PaymentModel, Service 
from datetime import date, datetime
from decimal import Decimal

def seed():
    with Session(engine) as session:
        admin = Administrator(username="admin", password_hash="123", role="manager")
        guest = Guest(first_name="Иван", last_name="Иванов", email="ivan@example.com")
        room = RoomModel(number="101", type="single", price_per_night=Decimal("50.00"), max_guests=1)  # ИЗМЕНЕНО

        session.add_all([admin, guest, room])
        session.commit()

        booking = Booking(
            guest_id=guest.id,
            room_id=room.id,
            admin_id=admin.id,
            check_in_date=date(2025,9,25),
            check_out_date=date(2025,9,28),
            status="confirmed",
            total_price=Decimal("150.00"),
            guests_count=1
        )
        session.add(booking)
        session.commit()

        payment = PaymentModel( 
            booking_id=booking.id,
            amount=Decimal("150.00"),
            status="paid",
            payment_method="card",
            transaction_id="tx-0001",
            paid_at=datetime.utcnow()
        )
        service = Service(
            type="spa",
            employee="Olga",
            status="scheduled",
            service_time=datetime.utcnow(),
            guest_id=guest.id,
            booking_id=booking.id
        )
        session.add_all([payment, service])
        session.commit()
    print("Данные добавлены.")

if __name__ == "__main__":
    seed()