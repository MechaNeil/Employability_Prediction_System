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
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.2/css/all.min.css" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" />
        <style>
          :root {
            --deep-1: #08183c;
            --deep-2: #173f89;
            --surface: #f3f5fa;
            --card: #ffffff;
            --ink: #1c2842;
            --muted: #67748e;
            --line: #dbe2f3;
            --blue: #2f66ff;
            --green: #10a86d;
            --purple: #7a39d8;
            --orange: #f28a1b;
            --nav-1: #081633;
            --nav-2: #102a5f;
            --shadow: 0 12px 24px rgba(20, 33, 65, 0.12);
          }

          * { box-sizing: border-box; }

          body {
            margin: 0;
            font-family: "Manrope", "Segoe UI", sans-serif;
            color: var(--ink);
            background: linear-gradient(130deg, var(--deep-1), var(--deep-2));
          }

          .topbar {
            color: #fff;
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
          }

          .title {
            margin: 0;
            font-family: "Sora", "Manrope", sans-serif;
            font-size: 48px;
            line-height: 0.95;
            letter-spacing: 0.2px;
          }

          .subtitle {
            margin: 4px 0 0;
            opacity: 0.95;
            font-size: 16px;
          }

          .online {
            border-radius: 999px;
            padding: 10px 16px;
            border: 1px solid rgba(27, 198, 131, 0.5);
            background: rgba(27, 198, 131, 0.2);
            color: #aef4d6;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 14px;
          }

          .layout {
            padding: 0 14px 14px;
            display: grid;
            grid-template-columns: 240px 1fr;
            gap: 14px;
            min-height: calc(100vh - 94px);
          }

          .sidebar {
            background: linear-gradient(180deg, var(--nav-1), var(--nav-2));
            border-radius: 16px;
            padding: 16px 12px;
            color: #dce5ff;
            box-shadow: var(--shadow);
          }

          .group-title {
            margin: 10px 10px 8px;
            font-size: 12px;
            color: #9ab0df;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
          }

          .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 11px 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 18px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.04);
          }

          .nav-item.active {
            background: linear-gradient(90deg, #2f66ff, #2457dc);
            color: #fff;
          }

          .nav-icon {
            width: 24px;
            height: 24px;
            border-radius: 7px;
            background: rgba(255, 255, 255, 0.15);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
          }

          .main {
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
            background: var(--card);
            border-radius: 14px;
            padding: 14px;
            box-shadow: var(--shadow);
            animation: lift 0.45s ease forwards;
            transform: translateY(8px);
            opacity: 0;
          }

          .card-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
          }

          .model-id {
            display: flex;
            align-items: center;
            gap: 10px;
          }

          .model-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            font-size: 20px;
            font-weight: 700;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.45);
          }

          .model-icon.blue { background: #e9f1ff; color: var(--blue); }
          .model-icon.green { background: #e8f8f0; color: var(--green); }
          .model-icon.purple { background: #f0e8fc; color: var(--purple); }
          .model-icon.orange { background: #fff1de; color: var(--orange); }

          .model-name {
            margin: 0;
            font-size: 17px;
            line-height: 1.1;
          }

          .model-sub {
            margin: 2px 0 0;
            font-size: 13px;
            color: var(--muted);
          }

          .state {
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 12px;
            font-weight: 700;
            color: #fff;
            display: inline-flex;
            align-items: center;
            gap: 6px;
          }

          .state.online { background: #16a36d; }
          .state.wait { background: #8a95ad; }
          .state.updated { background: #6a79ff; }

          .metric {
            margin-top: 10px;
            font-size: 38px;
            font-weight: 700;
          }

          .metric.blue { color: var(--blue); }
          .metric.green { color: var(--green); }
          .metric.purple { color: var(--purple); }
          .metric.orange { color: var(--orange); }

          .tag {
            display: inline-block;
            margin-top: 3px;
            font-size: 12px;
            font-weight: 700;
            border-radius: 999px;
            padding: 4px 9px;
            color: #fff;
            display: inline-flex;
            align-items: center;
            gap: 6px;
          }

          .tag.good { background: #16a36d; }
          .tag.pending { background: #8a95ad; }

          .panel {
            background: #fff;
            border-radius: 14px;
            box-shadow: var(--shadow);
            padding: 14px;
          }

          .actions {
            margin-top: 12px;
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
          }

          .action {
            border: 0;
            border-radius: 12px;
            color: #fff;
            text-align: left;
            padding: 12px;
            cursor: pointer;
            transition: transform 0.12s ease, filter 0.12s ease;
          }

          .action:hover { transform: translateY(-1px); filter: brightness(1.05); }
          .action:disabled { opacity: 0.8; cursor: wait; }
          .action-title { font-size: 16px; font-weight: 700; }
          .action-sub { margin-top: 2px; font-size: 12px; opacity: 0.92; }
          .action-title i { margin-right: 7px; }

          .a1 { background: linear-gradient(90deg, #2f66ff, #2658dd); }
          .a2 { background: linear-gradient(90deg, #14a263, #0f8250); }
          .a3 { background: linear-gradient(90deg, #f28a1b, #d36f12); }
          .a4 { background: linear-gradient(90deg, #7a39d8, #632abf); }
          .a5 { background: linear-gradient(90deg, #3f4d68, #2b354b); }

          .row {
            margin-top: 12px;
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 12px;
          }

          .panel-title {
            margin: 0 0 10px;
            font-size: 20px;
          }

          .chart {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            align-items: end;
            gap: 10px;
            min-height: 250px;
            padding: 8px;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: linear-gradient(180deg, #fafcff, #f2f6ff);
          }

          .bar-wrap { text-align: center; }

          .bar-value {
            display: inline-block;
            margin-bottom: 8px;
            padding: 4px 8px;
            border-radius: 8px;
            min-width: 58px;
            color: #fff;
            background: #1b2745;
            font-size: 12px;
            font-weight: 700;
          }

          .bar {
            width: 100%;
            max-width: 96px;
            margin: 0 auto;
            border-radius: 10px 10px 4px 4px;
            min-height: 6px;
          }

          .bar.blue { background: linear-gradient(180deg, #4f84ff, #2f66ff); }
          .bar.green { background: linear-gradient(180deg, #31c587, #10a86d); }
          .bar.purple { background: linear-gradient(180deg, #a063e8, #7a39d8); }
          .bar.orange { background: linear-gradient(180deg, #f9a947, #f28a1b); }

          .bar-label {
            margin-top: 8px;
            font-size: 13px;
            color: #33405d;
            font-weight: 700;
          }

          .timeline {
            border-left: 2px solid #d8e3f7;
            margin-left: 8px;
            padding-left: 14px;
          }

          .step {
            position: relative;
            margin-bottom: 10px;
          }

          .step::before {
            content: "";
            position: absolute;
            left: -20px;
            top: 4px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #c4cedf;
          }

          .step.ok::before { background: #13ab6d; }
          .step.bad::before { background: #ea5757; }

          .step-title {
            font-size: 15px;
            font-weight: 700;
            color: #223154;
            display: inline-flex;
            align-items: center;
            gap: 8px;
          }

          .step-sub {
            margin-top: 1px;
            font-size: 13px;
            color: #66748f;
          }

          .log {
            margin-top: 12px;
            background: #0f182d;
            color: #d9e9ff;
            border-radius: 12px;
            padding: 10px;
            font: 12px/1.4 Consolas, monospace;
            height: 154px;
            overflow: auto;
          }

          .footer {
            margin-top: 10px;
            font-size: 13px;
            color: #6f7d96;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 6px;
          }

          @keyframes lift {
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }

          @media (max-width: 1260px) {
            .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .actions { grid-template-columns: repeat(3, minmax(0, 1fr)); }
          }

          @media (max-width: 980px) {
            .layout { grid-template-columns: 1fr; }
            .sidebar { padding: 12px; }
            .title { font-size: 36px; }
            .row { grid-template-columns: 1fr; }
          }

          @media (max-width: 680px) {
            .topbar { padding: 14px; }
            .title { font-size: 30px; }
            .layout { padding: 0 10px 10px; }
            .main { padding: 10px; }
            .cards { grid-template-columns: 1fr; }
            .actions { grid-template-columns: 1fr; }
            .chart { min-height: 220px; }
            .metric { font-size: 32px; }
            .nav-item { font-size: 16px; }
            .online { padding: 8px 12px; }
          }
        </style>
      </head>
      <body>
        <header class="topbar">
          <div>
            <h1 class="title">Federated Learning System</h1>
            <p class="subtitle">Central Model Dashboard</p>
          </div>
          <div class="online" id="systemBadge"><i class="fa-solid fa-circle-check"></i>System Online</div>
        </header>

        <div class="layout">
          <aside class="sidebar">
            <div class="nav-item active"><span class="nav-icon"><i class="fa-solid fa-table-cells-large"></i></span>Dashboard</div>
            <div class="group-title">Model Workflow</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-play"></i></span>Train Main Model</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-paper-plane"></i></span>Deploy to Hospitals</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-layer-group"></i></span>Aggregate Models</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-chart-line"></i></span>Evaluate Global</div>
            <div class="group-title">System</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-server"></i></span>API Status</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-scroll"></i></span>Logs</div>
          </aside>

          <main class="main">
            <section class="cards">
              <article class="card">
                <div class="card-head">
                  <div class="model-id">
                    <span class="model-icon blue"><i class="fa-solid fa-brain"></i></span>
                    <div>
                      <h4 class="model-name">Main Model</h4>
                      <p class="model-sub">Accuracy (Set-1)</p>
                    </div>
                  </div>
                  <span class="state updated"><i class="fa-solid fa-wand-magic-sparkles"></i>updated</span>
                </div>
                <div id="mainAcc" class="metric blue">-</div>
                <span id="mainTag" class="tag pending">Pending</span>
              </article>

              <article class="card" style="animation-delay:0.06s">
                <div class="card-head">
                  <div class="model-id">
                    <span class="model-icon green"><i class="fa-solid fa-hospital"></i></span>
                    <div>
                      <h4 class="model-name">Hospital-1</h4>
                      <p class="model-sub">Local Model</p>
                    </div>
                  </div>
                  <span id="h1State" class="state wait"><i class="fa-solid fa-circle"></i>offline</span>
                </div>
                <div id="h1Acc" class="metric green">-</div>
                <span id="h1Tag" class="tag pending">Pending</span>
              </article>

              <article class="card" style="animation-delay:0.12s">
                <div class="card-head">
                  <div class="model-id">
                    <span class="model-icon purple"><i class="fa-solid fa-hospital-user"></i></span>
                    <div>
                      <h4 class="model-name">Hospital-2</h4>
                      <p class="model-sub">Local Model</p>
                    </div>
                  </div>
                  <span id="h2State" class="state wait"><i class="fa-solid fa-circle"></i>offline</span>
                </div>
                <div id="h2Acc" class="metric purple">-</div>
                <span id="h2Tag" class="tag pending">Pending</span>
              </article>

              <article class="card" style="animation-delay:0.18s">
                <div class="card-head">
                  <div class="model-id">
                    <span class="model-icon orange"><i class="fa-solid fa-earth-americas"></i></span>
                    <div>
                      <h4 class="model-name">Global Model</h4>
                      <p class="model-sub">Accuracy (v2)</p>
                    </div>
                  </div>
                  <span class="state updated"><i class="fa-solid fa-rocket"></i>v2</span>
                </div>
                <div id="globalAcc" class="metric orange">-</div>
                <span id="globalTag" class="tag pending">Pending</span>
              </article>
            </section>

            <section class="panel" style="margin-top:12px">
              <h3 class="panel-title">Action Controls</h3>
              <div class="actions">
                <button class="action a1" id="btnTrain" onclick="runAction('train')">
                  <div class="action-title"><i class="fa-solid fa-play"></i>Train Main Model</div>
                  <div class="action-sub">Using Set-1</div>
                </button>
                <button class="action a2" id="btnDeploy" onclick="runAction('deploy')">
                  <div class="action-title"><i class="fa-solid fa-paper-plane"></i>Deploy to Hospitals</div>
                  <div class="action-sub">Send latest central model</div>
                </button>
                <button class="action a3" id="btnRetrain" onclick="runAction('retrain-hospitals')">
                  <div class="action-title"><i class="fa-solid fa-arrows-rotate"></i>Trigger Retraining</div>
                  <div class="action-sub">H1: Set-2 | H2: Set-3</div>
                </button>
                <button class="action a4" id="btnAggregate" onclick="runAction('aggregate')">
                  <div class="action-title"><i class="fa-solid fa-layer-group"></i>Aggregate Models</div>
                  <div class="action-sub">Create Global v2</div>
                </button>
                <button class="action a5" id="btnEvaluate" onclick="runAction('evaluate')">
                  <div class="action-title"><i class="fa-solid fa-chart-column"></i>Evaluate Global</div>
                  <div class="action-sub">Test on holdout set</div>
                </button>
              </div>
            </section>

            <section class="row">
              <div class="panel">
                <h3 class="panel-title">Model Performance Comparison</h3>
                <div id="chart" class="chart"></div>
              </div>
              <div class="panel">
                <h3 class="panel-title">Workflow Status</h3>
                <div class="timeline">
                  <div id="stepMain" class="step"><div class="step-title"><i class="fa-solid fa-brain"></i>Main Model Trained</div><div class="step-sub">Random Forest on Set-1</div></div>
                  <div id="stepDeploy" class="step"><div class="step-title"><i class="fa-solid fa-paper-plane"></i>Model Deployed</div><div class="step-sub">Ready for remote retraining</div></div>
                  <div id="stepH1" class="step"><div class="step-title"><i class="fa-solid fa-hospital"></i>Hospital-1 Online</div><div class="step-sub">Service + local model endpoint</div></div>
                  <div id="stepH2" class="step"><div class="step-title"><i class="fa-solid fa-hospital-user"></i>Hospital-2 Online</div><div class="step-sub">Service + local model endpoint</div></div>
                  <div id="stepGlobal" class="step"><div class="step-title"><i class="fa-solid fa-earth-americas"></i>Aggregation Complete</div><div class="step-sub">Global model v2 generated</div></div>
                </div>
              </div>
            </section>

            <div id="activityLog" class="log"></div>

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

          function setStep(id, ok) {
            const node = document.getElementById(id);
            node.className = `step ${ok ? 'ok' : 'bad'}`;
          }

          function setTag(id, text, ok) {
            const node = document.getElementById(id);
            node.innerHTML = `${ok ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-hourglass-half"></i>'}${text}`;
            node.className = `tag ${ok ? 'good' : 'pending'}`;
          }

          function setState(id, text, kind) {
            const node = document.getElementById(id);
            node.innerHTML = `${kind === 'online' ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-circle"></i>'}${text}`;
            node.className = `state ${kind}`;
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
                const label = item.value === null ? 'N/A' : `${pct.toFixed(1)}%`;
                const h = Math.max(6, Math.round((pct / 100) * 190));
                return `
                  <div class="bar-wrap">
                    <div class="bar-value">${label}</div>
                    <div class="bar ${item.color}" style="height:${h}px"></div>
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
              const mainReady = status.models?.base_model?.exists === true;
              const globalReady = status.models?.global_model?.exists === true;
              const cmp = status.comparison || {};

              const mainPct = toPercent(cmp.main);
              const h1Pct = toPercent(cmp.hospital_1);
              const h2Pct = toPercent(cmp.hospital_2);
              const globalPct = toPercent(cmp.global);

              document.getElementById('mainAcc').textContent = mainPct ? `${mainPct}%` : '-';
              document.getElementById('h1Acc').textContent = h1Pct ? `${h1Pct}%` : '-';
              document.getElementById('h2Acc').textContent = h2Pct ? `${h2Pct}%` : '-';
              document.getElementById('globalAcc').textContent = globalPct ? `${globalPct}%` : '-';

              setTag('mainTag', mainReady ? 'Trained' : 'Pending', mainReady);
              setTag('h1Tag', h1 ? 'Online' : 'Offline', h1);
              setTag('h2Tag', h2 ? 'Online' : 'Offline', h2);
              setTag('globalTag', globalReady ? 'Aggregated' : 'Pending', globalReady);

              setState('h1State', h1 ? 'online' : 'offline', h1 ? 'online' : 'wait');
              setState('h2State', h2 ? 'online' : 'offline', h2 ? 'online' : 'wait');

              setStep('stepMain', mainReady);
              setStep('stepDeploy', mainReady && h1 && h2);
              setStep('stepH1', h1);
              setStep('stepH2', h2);
              setStep('stepGlobal', globalReady);

              const systemBadge = document.getElementById('systemBadge');
              systemBadge.innerHTML = h1 && h2
                ? '<i class="fa-solid fa-circle-check"></i>System Online'
                : '<i class="fa-solid fa-triangle-exclamation"></i>Partial Connectivity';

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
              const res = await fetch(endpoint.path, { method: endpoint.method });
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
