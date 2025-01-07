from fastapi import FastAPI
from app.api.v1 import users, products, orders

app = FastAPI(title="BackParts Marketplace")

#* Routes for start
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return{"msg": "Sijak"}