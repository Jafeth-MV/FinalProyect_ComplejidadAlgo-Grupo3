from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from infrastructure.api.routers import optimization

app = FastAPI(
    title="RutaFix API",
    description="API para el sistema de optimización de rutas",
    version="2.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(optimization.router, prefix="/api", tags=["Optimization"])

@app.get("/")
def read_root():
    return {"message": "RutaFix API is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("infrastructure.api.main:app", host="0.0.0.0", port=port, reload=True)
