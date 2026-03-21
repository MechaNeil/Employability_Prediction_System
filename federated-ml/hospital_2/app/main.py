from fastapi import FastAPI

from hospital_2.app.api.routes import router

app = FastAPI(title="Hospital-2 Server")
app.include_router(router)
