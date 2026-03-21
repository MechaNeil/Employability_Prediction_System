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
            --bg-a: #0b1d44;
            --bg-b: #173e87;
            --surface: #f4f6fb;
            --panel: #ffffff;
            --ink: #1b2640;
            --muted: #60708d;
            --blue: #2f66ff;
            --green: #0ea56a;
            --purple: #7e39d9;
            --orange: #f28a1b;
            --nav: #0a1a3c;
            --nav-2: #102a5c;
            --shadow: 0 10px 28px rgba(23, 37, 70, 0.11);
          }

          * {
            box-sizing: border-box;
          }

          body {
            margin: 0;
            font-family: "Trebuchet MS", "Segoe UI", sans-serif;
            color: var(--ink);
            background: linear-gradient(135deg, var(--bg-a), var(--bg-b));
            min-height: 100vh;
          }

          .topbar {
            padding: 18px 26px;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
          }

          .topbar h1 {
            margin: 0;
            font-size: 40px;
            line-height: 1;
            letter-spacing: 0.1px;
          }

          .topbar p {
            margin: 4px 0 0;
            opacity: 0.92;
            font-size: 16px;
          }

          .badge-online {
            background: rgba(7, 177, 112, 0.25);
            color: #adf3d3;
            border: 1px solid rgba(7, 177, 112, 0.5);
            padding: 10px 16px;
            border-radius: 999px;
            font-size: 15px;
            font-weight: 700;
          }

          .layout {
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 14px;
            padding: 0 14px 14px;
          }

          .nav {
            background: linear-gradient(180deg, var(--nav), var(--nav-2));
            border-radius: 16px;
            color: #d7e3ff;
            padding: 20px 16px;
            min-height: calc(100vh - 120px);
            box-shadow: var(--shadow);
          }

          .nav h3 {
            margin: 4px 10px 10px;
            color: #fff;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.85;
          }

          .nav .item {
            padding: 12px 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.04);
            font-size: 22px;
            font-weight: 700;
          }

          .nav .item.active {
            background: linear-gradient(90deg, #2a63f4, #2454d3);
            color: #fff;
          }

          .content {
            background: var(--surface);
            border-radius: 16px;
            padding: 14px;
            box-shadow: var(--shadow);
          }

          .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
          }

          .card {
            background: var(--panel);
            border-radius: 16px;
            padding: 16px;
            box-shadow: var(--shadow);
            transform: translateY(8px);
            opacity: 0;
            animation: rise 0.45s ease forwards;
          }

          .card h4 {
            margin: 0;
            font-size: 29px;
            line-height: 1.05;
          }

          .card p {
            margin: 6px 0 0;
            color: var(--muted);
            font-size: 20px;
            font-weight: 600;
          }

          .metric {
            font-size: 43px;
            margin-top: 10px;
            font-weight: 700;
          }

          .pill {
            display: inline-block;
            margin-top: 6px;
            font-size: 15px;
            font-weight: 700;
            border-radius: 999px;
            padding: 4px 10px;
            color: #fff;
          }

          .pill.green { background: #18a56d; }
          .pill.orange { background: #eb8418; }
          .pill.gray { background: #6e7a94; }

          .blue { color: var(--blue); }
          .green { color: var(--green); }
          .purple { color: var(--purple); }
          .orange { color: var(--orange); }

          .actions {
            margin-top: 12px;
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
          }

          .btn {
            border: 0;
            border-radius: 12px;
            color: #fff;
            font-weight: 700;
            font-size: 17px;
            padding: 14px 10px;
            cursor: pointer;
            transition: transform 0.12s ease, filter 0.12s ease;
          }

          .btn:disabled {
            cursor: wait;
            filter: grayscale(0.2);
            opacity: 0.8;
          }

          .btn:hover {
            transform: translateY(-1px);
            filter: brightness(1.05);
          }

          .b1 { background: linear-gradient(90deg, #2f66ff, #315ce0); }
          .b2 { background: linear-gradient(90deg, #12a162, #0e8451); }
          .b3 { background: linear-gradient(90deg, #f28a1b, #d16d10); }
          .b4 { background: linear-gradient(90deg, #7b3fd3, #5f26b8); }
          .b5 { background: linear-gradient(90deg, #3f4d68, #2b354b); }

          .grid-2 {
            margin-top: 12px;
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 12px;
          }

          .panel {
            background: #fff;
            border-radius: 16px;
            padding: 14px;
            box-shadow: var(--shadow);
          }

          .panel h3 {
            margin: 0 0 10px;
            font-size: 20px;
          }

          .chart {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            align-items: end;
            height: 250px;
            padding: 10px 8px 6px;
            background: linear-gradient(180deg, #f9fbff, #f1f5ff);
            border-radius: 12px;
            border: 1px solid #e4ebfa;
          }

          .bar-wrap {
            text-align: center;
          }

          .bar {
            width: 100%;
            max-width: 100px;
            margin: 0 auto;
            border-radius: 10px 10px 4px 4px;
            min-height: 6px;
            position: relative;
          }

          .bar.blue { background: linear-gradient(180deg, #4d82ff, #2f66ff); }
          .bar.green { background: linear-gradient(180deg, #28be82, #0ea56a); }
          .bar.purple { background: linear-gradient(180deg, #9959e5, #7e39d9); }
          .bar.orange { background: linear-gradient(180deg, #f8a33c, #f28a1b); }

          .bar-value {
            margin-bottom: 8px;
            background: #1b2745;
            color: #fff;
            display: inline-block;
            font-size: 13px;
            padding: 4px 8px;
            border-radius: 8px;
            min-width: 58px;
          }

          .bar-label {
            margin-top: 8px;
            font-size: 14px;
            color: #33405d;
            font-weight: 700;
          }

          .log {
            background: #101829;
            color: #dbecff;
            border-radius: 12px;
            padding: 10px;
            font-size: 13px;
            height: 160px;
            overflow: auto;
            font-family: Consolas, monospace;
          }

          .status-item {
            margin-bottom: 8px;
            font-size: 15px;
            color: #2f3e5e;
            font-weight: 600;
          }

          .dot {
            display: inline-block;
            width: 11px;
            height: 11px;
            border-radius: 50%;
            margin-right: 8px;
            background: #bbb;
          }

          .ok { background: #14b86a; }
          .bad { background: #ef5656; }

          .footer {
            margin-top: 10px;
            font-size: 13px;
            color: #6f7d96;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 6px;
          }

          @keyframes rise {
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }

          @media (max-width: 1240px) {
            .cards {
              grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .actions {
              grid-template-columns: repeat(3, minmax(0, 1fr));
            }
          }

          @media (max-width: 990px) {
            .layout { grid-template-columns: 1fr; }
            .nav { min-height: auto; }
            .grid-2 { grid-template-columns: 1fr; }
            .topbar h1 { font-size: 32px; }
          }

          @media (max-width: 640px) {
            .topbar { padding: 14px; }
            .topbar h1 { font-size: 28px; }
            .layout { padding: 0 10px 10px; }
            .content { padding: 10px; }
            .cards { grid-template-columns: 1fr; }
            .actions { grid-template-columns: 1fr; }
            .chart { height: 220px; }
            .metric { font-size: 34px; }
            .card h4 { font-size: 25px; }
            .card p { font-size: 17px; }
            .nav .item { font-size: 18px; }
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
            <div class="item active">Dashboard</div>
            <h3>Model Workflow</h3>
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
                <p>Accuracy (Set-1)</p>
                <div id="mainAcc" class="metric blue">-</div>
                <div id="mainTag" class="pill gray">Pending</div>
              </div>
              <div class="card" style="animation-delay:0.08s">
                <h4>Hospital-1</h4>
                <p>Local model</p>
                <div id="h1Acc" class="metric green">-</div>
                <div id="h1Tag" class="pill gray">Pending</div>
              </div>
              <div class="card" style="animation-delay:0.16s">
                <h4>Hospital-2</h4>
                <p>Local model</p>
                <div id="h2Acc" class="metric purple">-</div>
                <div id="h2Tag" class="pill gray">Pending</div>
              </div>
              <div class="card" style="animation-delay:0.24s">
                <h4>Global Model</h4>
                <p>Accuracy (v2)</p>
                <div id="globalAcc" class="metric orange">-</div>
                <div id="globalTag" class="pill gray">Pending</div>
              </div>
            </section>

            <section class="actions">
              <button class="btn b1" id="btnTrain" onclick="runAction('train')">Train Main Model</button>
              <button class="btn b2" id="btnDeploy" onclick="runAction('deploy')">Deploy to Hospitals</button>
              <button class="btn b3" id="btnRetrain" onclick="runAction('retrain-hospitals')">Trigger Retraining</button>
              <button class="btn b4" id="btnAggregate" onclick="runAction('aggregate')">Aggregate Models</button>
              <button class="btn b5" id="btnEvaluate" onclick="runAction('evaluate')">Evaluate Global</button>
            </section>

            <section class="grid-2">
              <div class="panel">
                <h3>Model Performance Comparison</h3>
                <div class="chart" id="chart"></div>
              </div>
              <div class="panel">
                <h3>Workflow Status</h3>
                <div class="status-item"><span id="dotMain" class="dot"></span>Main model trained</div>
                <div class="status-item"><span id="dotDeploy" class="dot"></span>Model deployed</div>
                <div class="status-item"><span id="dotH1" class="dot"></span>Hospital-1 online</div>
                <div class="status-item"><span id="dotH2" class="dot"></span>Hospital-2 online</div>
                <div class="status-item"><span id="dotGlobal" class="dot"></span>Aggregation complete</div>
              </div>
            </section>

            <section class="panel" style="margin-top:12px">
              <h3>Activity Log</h3>
              <div id="activityLog" class="log"></div>
            </section>

            <div class="footer">
              <span>Federated Learning System | Central Server - FastAPI</span>
              <span id="lastUpdated">Last updated: -</span>
            </div>
          </main>
        </div>

        <script>
          const logEl = document.getElementById('activityLog');

          function writeLog(message) {
            const stamp = new Date().toLocaleTimeString();
            logEl.textContent = `[${stamp}] ${message}\n` + logEl.textContent;
            document.getElementById('lastUpdated').textContent = `Last updated: ${stamp}`;
          }

          function setDot(id, ok) {
            const el = document.getElementById(id);
            el.className = `dot ${ok ? 'ok' : 'bad'}`;
          }

          function setTag(id, text, ok) {
            const tag = document.getElementById(id);
            tag.textContent = text;
            tag.className = `pill ${ok ? 'green' : 'gray'}`;
          }

          function toPercent(value) {
            if (value === null || value === undefined) {
              return null;
            }
            return (value * 100).toFixed(1);
          }

          function renderBars(main, h1, h2, global) {
            const chart = document.getElementById('chart');
            const values = [
              { key: 'Main Model', value: main, color: 'blue' },
              { key: 'Hospital-1', value: h1, color: 'green' },
              { key: 'Hospital-2', value: h2, color: 'purple' },
              { key: 'Global Model v2', value: global, color: 'orange' },
            ];

            chart.innerHTML = values
              .map((item) => {
                const pct = item.value === null ? 0 : Math.max(0, Math.min(100, item.value));
                const height = Math.max(6, Math.round((pct / 100) * 180));
                const label = item.value === null ? 'N/A' : `${pct.toFixed(1)}%`;
                return `
                  <div class="bar-wrap">
                    <div class="bar-value">${label}</div>
                    <div class="bar ${item.color}" style="height:${height}px"></div>
                    <div class="bar-label">${item.key}</div>
                  </div>
                `;
              })
              .join('');
          }

          function setButtonsBusy(isBusy) {
            ['btnTrain', 'btnDeploy', 'btnRetrain', 'btnAggregate', 'btnEvaluate'].forEach((id) => {
              const button = document.getElementById(id);
              if (button) {
                button.disabled = isBusy;
              }
            });
          }

          function endpointFor(action) {
            if (action === 'train') return { path: '/train', method: 'POST' };
            if (action === 'deploy') return { path: '/deploy', method: 'POST' };
            if (action === 'retrain-hospitals') return { path: '/retrain-hospitals', method: 'POST' };
            if (action === 'aggregate') return { path: '/aggregate', method: 'GET' };
            if (action === 'evaluate') return { path: '/evaluate', method: 'GET' };
            return { path: '/status', method: 'GET' };
          }

          async function refreshStatus() {
            try {
              const status = await fetch('/status').then((r) => r.json());
              const h1 = status.hospitals?.hospital_1?.online === true;
              const h2 = status.hospitals?.hospital_2?.online === true;
              const mainExists = status.models?.base_model?.exists === true;
              const globalExists = status.models?.global_model?.exists === true;
              const cmp = status.comparison || {};

              const mainPct = toPercent(cmp.main);
              const h1Pct = toPercent(cmp.hospital_1);
              const h2Pct = toPercent(cmp.hospital_2);
              const globalPct = toPercent(cmp.global);

              setDot('dotMain', mainExists);
              setDot('dotDeploy', mainExists && h1 && h2);
              setDot('dotH1', h1);
              setDot('dotH2', h2);
              setDot('dotGlobal', globalExists);

              document.getElementById('mainAcc').textContent = mainPct ? `${mainPct}%` : '-';
              document.getElementById('h1Acc').textContent = h1Pct ? `${h1Pct}%` : '-';
              document.getElementById('h2Acc').textContent = h2Pct ? `${h2Pct}%` : '-';
              document.getElementById('globalAcc').textContent = globalPct ? `${globalPct}%` : '-';

              setTag('mainTag', mainExists ? 'Trained' : 'Pending', mainExists);
              setTag('h1Tag', h1 ? 'Online' : 'Offline', h1);
              setTag('h2Tag', h2 ? 'Online' : 'Offline', h2);
              setTag('globalTag', globalExists ? 'Aggregated' : 'Pending', globalExists);

              document.getElementById('systemBadge').textContent = (h1 && h2) ? 'System Online' : 'Partial Connectivity';

              renderBars(
                mainPct ? Number(mainPct) : null,
                h1Pct ? Number(h1Pct) : null,
                h2Pct ? Number(h2Pct) : null,
                globalPct ? Number(globalPct) : null,
              );
              writeLog('Status refreshed.');
            } catch (error) {
              writeLog(`Status refresh failed: ${error}`);
            }
          }

          async function runAction(action) {
            try {
              setButtonsBusy(true);
              const endpoint = endpointFor(action);
              const path = endpoint.path;
              const method = endpoint.method;
              const res = await fetch(path, { method });
              const body = await res.json();
              if (!res.ok) {
                throw new Error(body.detail || JSON.stringify(body));
              }
              writeLog(`${action.toUpperCase()} success: ${JSON.stringify(body)}`);
              await refreshStatus();
            } catch (error) {
              writeLog(`${action.toUpperCase()} failed: ${error}`);
            } finally {
              setButtonsBusy(false);
            }
          }

          refreshStatus();
          setInterval(refreshStatus, 15000);
        </script>
      </body>
    </html>
    """
