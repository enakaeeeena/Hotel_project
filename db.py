from sqlmodel import SQLModel, create_engine
from models import Guest, Administrator, RoomModel, Booking, PaymentModel, Service

DATABASE_URL = "postgresql+psycopg2://hotel_user:Oleded2412@localhost:5432/hotel_db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.schema = "public"
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session