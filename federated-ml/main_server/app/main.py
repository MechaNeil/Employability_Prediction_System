from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from main_server.app.api.routes import router

app = FastAPI(title="Federated Learning Main Server")
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def dashboard_placeholder() -> str:
    return """
    <html>
      <head>
        <title>Federated Learning Dashboard</title>
        <style>
          body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f1f3d, #1f4a8a); color: #f0f4ff; margin: 0; }
          .wrap { max-width: 900px; margin: 80px auto; padding: 24px; background: rgba(10, 20, 40, 0.75); border-radius: 14px; }
          h1 { margin-top: 0; }
          ul { line-height: 1.8; }
          code { color: #9bd2ff; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <h1>Federated Learning System</h1>
          <p>Backend is ready. Use these endpoints:</p>
          <ul>
            <li><code>POST /train</code> - train initial main model on Set-1</li>
            <li><code>GET /aggregate</code> - trigger hospital retrain + model aggregation</li>
            <li><code>GET /evaluate</code> - evaluate final global model on test set</li>
            <li><code>GET /health</code> - service status</li>
          </ul>
        </div>
      </body>
    </html>
    """
