from fastapi import FastAPI

from hospital_1.app.api.routes import router

app = FastAPI(title="Hospital-1 Server")
app.include_router(router)
