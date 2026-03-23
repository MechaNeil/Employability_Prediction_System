from fastapi import FastAPI

from employability_1.app.api.routes import router

app = FastAPI(title="Employability-1 Server")
app.include_router(router)

