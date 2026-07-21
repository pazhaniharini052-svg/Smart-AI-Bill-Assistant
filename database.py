from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(
    "sqlite:///bills.db",
    connect_args={"check_same_thread": False}
)


Base = declarative_base()


class Bill(Base):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)

    store_name = Column(String)
    date = Column(String)
    invoice_number = Column(String)

    total_amount = Column(Float)
    gst = Column(Float)

    items = Column(Text)

    file_path = Column(String)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)