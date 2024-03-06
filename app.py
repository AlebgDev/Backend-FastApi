from fastapi import FastAPI
from routes.product import product

app = FastAPI()

app.include_router(product)