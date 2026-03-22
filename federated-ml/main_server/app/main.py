import logging

from fastapi import FastAPI

from main_server.app.api.routes import router

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Federated Learning Main Server")
app.include_router(router)
