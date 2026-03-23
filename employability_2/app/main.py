from fastapi import FastAPI

from employability_2.app.api.routes import router

app = FastAPI(title="Employability-2 Server")
app.include_router(router)

