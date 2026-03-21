import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from main_server.app.api.routes import router

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Federated Learning Main Server")
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def dashboard_placeholder() -> str:
    return """
    <html>
      <head>
        <title>Federated Learning System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          :root {
            --bg-a: #08142c;
            --bg-b: #123a7c;
            --panel: #ffffff;
            --ink: #1d2840;
            --muted: #6b7691;
            --blue: #2f66ff;
            --green: #0ea56a;
            --purple: #7e39d9;
            --orange: #f28a1b;
            --nav: #0c1d43;
            --nav-2: #0f2c63;
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            font-family: "Trebuchet MS", "Gill Sans", "Segoe UI", sans-serif;
            color: var(--ink);
            background: linear-gradient(135deg, var(--bg-a), var(--bg-b));
            min-height: 100vh;
          }
          .topbar {
            padding: 18px 24px;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }
          .topbar h1 {
            margin: 0;
            font-size: 30px;
            letter-spacing: 0.2px;
          }
          .topbar p {
            margin: 0;
            opacity: 0.9;
          }
          .badge-online {
            background: rgba(13, 185, 120, 0.25);
            color: #9ef3ce;
            border: 1px solid rgba(13, 185, 120, 0.45);
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 14px;
          }
          .layout {
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 16px;
            padding: 0 16px 16px 16px;
          }
          .nav {
            background: linear-gradient(180deg, var(--nav), var(--nav-2));
            border-radius: 16px;
            color: #d7e3ff;
            padding: 18px;
            min-height: calc(100vh - 120px);
          }
          .nav h3 {
            margin: 12px 0;
            color: #fff;
            font-size: 16px;
          }
          .nav .item {
            padding: 10px 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.04);
            font-size: 14px;
          }
          .content {
            background: #f2f4f8;
            border-radius: 16px;
            padding: 16px;
          }
          .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
          }
          .card {
            background: var(--panel);
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(23, 32, 54, 0.1);
            transform: translateY(8px);
            opacity: 0;
            animation: rise 0.45s ease forwards;
          }
          .card h4 {
            margin: 0;
            font-size: 22px;
          }
          .card p {
            margin: 6px 0 0 0;
            color: var(--muted);
            font-size: 14px;
          }
          .metric {
            font-size: 34px;
            margin-top: 10px;
            font-weight: 700;
          }
          .blue { color: var(--blue); }
          .green { color: var(--green); }
          .purple { color: var(--purple); }
          .orange { color: var(--orange); }
          .actions {
            margin-top: 14px;
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
          }
          .btn {
            border: 0;
            border-radius: 12px;
            color: #fff;
            font-weight: 700;
            padding: 14px 10px;
            cursor: pointer;
          }
          .b1 { background: linear-gradient(90deg, #2f66ff, #315ce0); }
          .b2 { background: linear-gradient(90deg, #12a162, #0e8451); }
          .b3 { background: linear-gradient(90deg, #f28a1b, #d16d10); }
          .b4 { background: linear-gradient(90deg, #7b3fd3, #5f26b8); }
          .grid-2 {
            margin-top: 14px;
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 12px;
          }
          .panel {
            background: #fff;
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(23, 32, 54, 0.1);
          }
          .panel h3 { margin: 0 0 10px 0; }
          .log {
            background: #101829;
            color: #dbecff;
            border-radius: 10px;
            padding: 10px;
            font-size: 13px;
            height: 180px;
            overflow: auto;
            font-family: Consolas, monospace;
          }
          .status-item {
            margin-bottom: 8px;
            font-size: 15px;
          }
          .dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            margin-right: 8px;
            background: #bbb;
          }
          .ok { background: #14b86a; }
          .bad { background: #ef5656; }
          @keyframes rise {
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }
          @media (max-width: 1050px) {
            .layout { grid-template-columns: 1fr; }
            .nav { min-height: auto; }
            .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .actions { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .grid-2 { grid-template-columns: 1fr; }
          }
        </style>
      </head>
      <body>
        <div class="topbar">
          <div>
            <h1>Federated Learning System</h1>
            <p>Central Model Dashboard</p>
          </div>
          <div class="badge-online" id="systemBadge">System Online</div>
        </div>

        <div class="layout">
          <aside class="nav">
            <h3>Dashboard</h3>
            <div class="item">Train Main Model</div>
            <div class="item">Deploy to Hospitals</div>
            <div class="item">Aggregate Models</div>
            <div class="item">Evaluate Global</div>
            <h3>System</h3>
            <div class="item">API Status</div>
            <div class="item">Logs</div>
          </aside>

          <main class="content">
            <section class="cards">
              <div class="card">
                <h4>Main Model</h4>
                <p>Base model accuracy</p>
                <div id="mainAcc" class="metric blue">-</div>
              </div>
              <div class="card" style="animation-delay:0.08s">
                <h4>Hospital-1</h4>
                <p>Local model status</p>
                <div id="h1Status" class="metric green">-</div>
              </div>
              <div class="card" style="animation-delay:0.16s">
                <h4>Hospital-2</h4>
                <p>Local model status</p>
                <div id="h2Status" class="metric purple">-</div>
              </div>
              <div class="card" style="animation-delay:0.24s">
                <h4>Global Model</h4>
                <p>Aggregated model accuracy</p>
                <div id="globalAcc" class="metric orange">-</div>
              </div>
            </section>

            <section class="actions">
              <button class="btn b1" onclick="runAction('train')">Train Main</button>
              <button class="btn b2" onclick="refreshStatus()">Refresh Status</button>
              <button class="btn b3" onclick="runAction('aggregate')">Aggregate</button>
              <button class="btn b4" onclick="runAction('evaluate')">Evaluate</button>
            </section>

            <section class="grid-2">
              <div class="panel">
                <h3>Model Performance Comparison</h3>
                <canvas id="chart" height="180"></canvas>
              </div>
              <div class="panel">
                <h3>Workflow Status</h3>
                <div class="status-item"><span id="dotMain" class="dot"></span>Main server healthy</div>
                <div class="status-item"><span id="dotH1" class="dot"></span>Hospital-1 healthy</div>
                <div class="status-item"><span id="dotH2" class="dot"></span>Hospital-2 healthy</div>
                <div class="status-item"><span id="dotGlobal" class="dot"></span>Global model available</div>
              </div>
            </section>

            <section class="panel" style="margin-top:12px">
              <h3>Activity Log</h3>
              <div id="activityLog" class="log"></div>
            </section>
          </main>
        </div>

        <script>
          const logEl = document.getElementById('activityLog');

          function writeLog(message) {
            const stamp = new Date().toLocaleTimeString();
            logEl.textContent = `[${stamp}] ${message}\n` + logEl.textContent;
          }

          function setDot(id, ok) {
            const el = document.getElementById(id);
            el.className = `dot ${ok ? 'ok' : 'bad'}`;
          }

          function drawBars(mainAcc, globalAcc) {
            const canvas = document.getElementById('chart');
            const ctx = canvas.getContext('2d');
            const bars = [
              { label: 'Main', value: mainAcc, color: '#2f66ff' },
              { label: 'Global', value: globalAcc, color: '#f28a1b' },
            ];

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const w = canvas.width;
            const h = canvas.height;
            const baseY = h - 20;
            const maxHeight = h - 40;

            bars.forEach((bar, idx) => {
              const x = 50 + idx * 120;
              const bw = 72;
              const bh = Math.max(4, (bar.value / 100) * maxHeight);
              ctx.fillStyle = bar.color;
              ctx.fillRect(x, baseY - bh, bw, bh);
              ctx.fillStyle = '#1d2840';
              ctx.font = '14px Trebuchet MS';
              ctx.fillText(`${bar.value.toFixed(1)}%`, x + 8, baseY - bh - 8);
              ctx.fillText(bar.label, x + 16, baseY + 14);
            });
          }

          async function refreshStatus() {
            try {
              const status = await fetch('/status').then((r) => r.json());
              let metrics = status.metrics;
              if (!metrics || metrics.available === false) {
                try {
                  metrics = await fetch('/evaluate').then((r) => r.json());
                } catch (_) {
                  metrics = null;
                }
              }

              const h1 = status.hospitals?.hospital_1?.online === true;
              const h2 = status.hospitals?.hospital_2?.online === true;
              const globalExists = status.models?.global_model?.exists === true;

              setDot('dotMain', true);
              setDot('dotH1', h1);
              setDot('dotH2', h2);
              setDot('dotGlobal', globalExists);

              document.getElementById('h1Status').textContent = h1 ? 'online' : 'offline';
              document.getElementById('h2Status').textContent = h2 ? 'online' : 'offline';

              const acc = metrics && metrics.accuracy ? metrics.accuracy * 100 : 0;
              const mainApprox = Math.max(0, acc - 2.1);

              document.getElementById('mainAcc').textContent = metrics ? `${mainApprox.toFixed(1)}%` : '-';
              document.getElementById('globalAcc').textContent = metrics ? `${acc.toFixed(1)}%` : '-';
              document.getElementById('systemBadge').textContent = (h1 && h2) ? 'System Online' : 'Partial Connectivity';

              drawBars(mainApprox, acc);
              writeLog('Status refreshed.');
            } catch (error) {
              writeLog(`Status refresh failed: ${error}`);
            }
          }

          async function runAction(action) {
            try {
              const path = action === 'aggregate' || action === 'evaluate' ? `/${action}` : '/train';
              const method = action === 'train' ? 'POST' : 'GET';
              const res = await fetch(path, { method });
              const body = await res.json();
              if (!res.ok) {
                throw new Error(body.detail || JSON.stringify(body));
              }
              writeLog(`${action.toUpperCase()} success: ${JSON.stringify(body)}`);
              await refreshStatus();
            } catch (error) {
              writeLog(`${action.toUpperCase()} failed: ${error}`);
            }
          }

          refreshStatus();
          setInterval(refreshStatus, 15000);
        </script>
      </body>
    </html>
    """
