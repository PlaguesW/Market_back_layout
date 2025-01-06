from fastapi import FastAPI
from app.api.v1 import users, products

app = FastAPI()


app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])

@app.get("/")
def read_root():
    return{"msg": "Sijak"}