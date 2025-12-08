from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

from sqlmodel import Session, select

from db import create_db_and_tables, engine
from models import Guest, RoomModel, Booking, PaymentModel, Service, Administrator

app = FastAPI(title="Hotel API", version="1.0")

# Создание таблиц при старте
create_db_and_tables()

# Зависимости

def get_db():
    with Session(engine) as session:
        yield session

# Схемы для обновления данных

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class GuestCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    passport_data: Optional[str] = None

class GuestUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    passport_data: Optional[str] = None

class RoomCreate(BaseModel):
    number: str
    type: Optional[str] = None
    description: Optional[str] = None
    price_per_night: Decimal
    max_guests: Optional[int] = None
    is_active: bool = True

class RoomUpdate(BaseModel):
    number: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    price_per_night: Optional[Decimal] = None
    max_guests: Optional[int] = None
    is_active: Optional[bool] = None

class BookingCreate(BaseModel):
    guest_id: Optional[int] = None
    room_id: Optional[int] = None
    admin_id: Optional[int] = None
    check_in_date: date
    check_out_date: date
    status: Optional[str] = None
    total_price: Decimal
    guests_count: Optional[int] = None

class BookingUpdate(BaseModel):
    guest_id: Optional[int] = None
    room_id: Optional[int] = None
    admin_id: Optional[int] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    status: Optional[str] = None
    total_price: Optional[Decimal] = None
    guests_count: Optional[int] = None

class PaymentCreate(BaseModel):
    booking_id: Optional[int] = None
    amount: Decimal
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None

class PaymentUpdate(BaseModel):
    booking_id: Optional[int] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None

class ServiceCreate(BaseModel):
    type: Optional[str] = None
    employee: Optional[str] = None
    status: Optional[str] = None
    service_time: Optional[datetime] = None
    guest_id: Optional[int] = None
    booking_id: Optional[int] = None

class ServiceUpdate(BaseModel):
    type: Optional[str] = None
    employee: Optional[str] = None
    status: Optional[str] = None
    service_time: Optional[datetime] = None
    guest_id: Optional[int] = None
    booking_id: Optional[int] = None

# Основные эндпоинты

@app.get("/")
def read_root():
    return {"message": "Hello, Hotel!"}

#Guests 
@app.get("/guests", response_model=List[Guest])
def get_all_guests(db: Session = Depends(get_db)):
    return db.exec(select(Guest)).all()

@app.get("/guests/{guest_id}", response_model=Guest)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

@app.post("/guests", response_model=Guest)
def create_guest(guest_data: GuestCreate, db: Session = Depends(get_db)):
    guest = Guest(**guest_data.dict())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

@app.put("/guests/{guest_id}", response_model=Guest)
def update_guest(guest_id: int, guest_data: GuestUpdate, db: Session = Depends(get_db)):
    guest = db.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    guest_data_dict = guest_data.dict(exclude_unset=True)
    for key, value in guest_data_dict.items():
        setattr(guest, key, value)
    
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

@app.delete("/guests/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.get(Guest, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    db.delete(guest)
    db.commit()
    return {"message": "Guest deleted successfully"}

# Bookings
@app.get("/bookings", response_model=List[Booking])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.exec(select(Booking)).all()

@app.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.post("/bookings", response_model=Booking)
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**booking_data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.put("/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, booking_data: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking_data_dict = booking_data.dict(exclude_unset=True)
    for key, value in booking_data_dict.items():
        setattr(booking, key, value)
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}

@app.get("/guests/{guest_id}/bookings", response_model=List[Booking])
def get_bookings_by_guest(guest_id: int, db: Session = Depends(get_db)):
    bookings = db.exec(
        select(Booking).where(Booking.guest_id == guest_id)
    ).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="Bookings not found")
    return bookings

# Rooms
@app.get("/rooms", response_model=List[RoomModel])
def get_available_rooms(db: Session = Depends(get_db)):
    return db.exec(select(RoomModel).where(RoomModel.is_active == True)).all()

@app.get("/rooms/{room_id}", response_model=RoomModel)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(RoomModel, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.post("/rooms", response_model=RoomModel)
def create_room(room_data: RoomCreate, db: Session = Depends(get_db)):
    room = RoomModel(**room_data.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@app.put("/rooms/{room_id}", response_model=RoomModel)
def update_room(room_id: int, room_data: RoomUpdate, db: Session = Depends(get_db)):
    room = db.get(RoomModel, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room_data_dict = room_data.dict(exclude_unset=True)
    for key, value in room_data_dict.items():
        setattr(room, key, value)
    
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(RoomModel, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}

# Services
@app.get("/services", response_model=List[Service])
def get_all_services(db: Session = Depends(get_db)):
    return db.exec(select(Service)).all()

@app.get("/services/{service_id}", response_model=Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.post("/services", response_model=Service)
def create_service(service_data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(**service_data.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@app.put("/services/{service_id}", response_model=Service)
def update_service(service_id: int, service_data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service_data_dict = service_data.dict(exclude_unset=True)
    for key, value in service_data_dict.items():
        setattr(service, key, value)
    
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}

@app.get("/guests/{guest_id}/services", response_model=List[Service])
def get_services_by_guest(guest_id: int, db: Session = Depends(get_db)):
    services = db.exec(
        select(Service).where(Service.guest_id == guest_id)
    ).all()
    if not services:
        raise HTTPException(status_code=404, detail="Services not found")
    return services

# Payments
@app.get("/payments", response_model=List[PaymentModel])
def get_all_payments(db: Session = Depends(get_db)):
    return db.exec(select(PaymentModel)).all()

@app.get("/payments/{payment_id}", response_model=PaymentModel)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.get(PaymentModel, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.post("/payments", response_model=PaymentModel)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    payment = PaymentModel(**payment_data.dict())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@app.put("/payments/{payment_id}", response_model=PaymentModel)
def update_payment(payment_id: int, payment_data: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.get(PaymentModel, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment_data_dict = payment_data.dict(exclude_unset=True)
    for key, value in payment_data_dict.items():
        setattr(payment, key, value)
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.get(PaymentModel, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}

@app.get("/bookings/{booking_id}/payments", response_model=List[PaymentModel])
def get_payments_by_booking(booking_id: int, db: Session = Depends(get_db)):
    payments = db.exec(
        select(PaymentModel).where(PaymentModel.booking_id == booking_id)
    ).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payments not found")
    return payments

# Administrators
@app.get("/administrators", response_model=List[Administrator])
def get_all_administrators(db: Session = Depends(get_db)):
    return db.exec(select(Administrator)).all()

# Детали бронирований
@app.get("/bookings/details")
def get_booking_details_endpoint(db: Session = Depends(get_db)):
    bookings = db.exec(select(Booking)).all()
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)