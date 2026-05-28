from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from database import SessionLocal, engine
from shared.auth import verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return {"message": "Product service running"}


@app.get("/products", response_model=list[schemas.ProductResponse])
async def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=schemas.ProductResponse)
async def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    return crud.create_product(db, product)


@app.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, product)
    return {"detail": f"Product {product_id} deleted", "deleted_by": current_user["sub"]}

