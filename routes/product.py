from fastapi import FastAPI, APIRouter, HTTPException
from config.db import conn
from models.product import products
from schemas.product import Product

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

product = APIRouter()


@product.get("/products", tags=["products"], response_model=list[Product])
def get_products():
    products_result = conn.execute(products.select()).fetchall()

    if not products_result:
        raise HTTPException(status_code=404, detail="No products found")

    return products_result


@product.post("/products", tags=["products"], response_model=Product, description="Create a new product")
def create_product(product: Product):
    print(product)
    new_product = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
    }
    print(new_product)
    result = conn.execute(products.insert().values(new_product))
    conn.commit()
    if result.rowcount == 1:
        return conn.execute(
            products.select().where(products.c.id == result.lastrowid)
        ).first()
    else:
        raise HTTPException(status_code=500, detail="Failed to insert product")


@product.get(
    "/products/{id}",
    tags=["products"],
    response_model=Product,
    description="Get a single user by Id",
)
def get_product(id: str):
    return conn.execute(products.select().where(products.c.id == id)).first()

@product.delete("/products/{id}")
def delete_product(id: int):
    result = conn.execute(products.delete().where(products.c.id == id))
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    conn.commit()  # Commit changes to the database
    return {"message": "Product deleted successfully"}

@product.put("/products/{id}", response_model=Product, description="Update a product by Id")
def update_product(product: Product, id: int):
    conn.execute(
        products.update()
        .values(name=product.name, description=product.description, price=product.price)
        .where(products.c.id == id)
    )
    conn.commit()  # Commit changes to the database
    updated_product = conn.execute(products.select().where(products.c.id == id)).first()

    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")

    return updated_product