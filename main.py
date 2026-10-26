import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class Product(Base):

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Integer)
    quantity = Column(Integer)


Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()




@app.post("/products/")
async def create_product(title: str, price: int, quantity: int):
    db = SessionLocal()
    db_product = Product(title=title, price=price, quantity=quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)  
    return db_product   

@app.get("/products/")
async def read_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return products



if __name__ == "__main__":
    uvicorn.run(app)
