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
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
          }

          .title {
            margin: 0;
            font-family: "Sora", "Manrope", sans-serif;
            font-size: 40px;
            line-height: 1;
            letter-spacing: 0.2px;
          }

          .subtitle {
            margin: 6px 0 0;
            opacity: 0.95;
            font-size: 15px;
          }

          .online {
            border-radius: 999px;
            padding: 9px 14px;
            border: 1px solid rgba(27, 198, 131, 0.5);
            background: rgba(27, 198, 131, 0.2);
            color: #aef4d6;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 13px;
          }

          .layout {
            padding: 0 12px 12px;
            display: grid;
            grid-template-columns: 240px 1fr;
            gap: 12px;
            min-height: calc(100vh - 94px);
          }

          .sidebar {
            background: linear-gradient(180deg, var(--nav-1), var(--nav-2));
            border-radius: 16px;
            padding: 14px 10px;
            color: #dce5ff;
            box-shadow: var(--shadow);
          }

          .group-title {
            margin: 12px 10px 8px;
            font-size: 12px;
            color: #9ab0df;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
          }

          .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.04);
          }

          .nav-button {
            width: 100%;
            border: 0;
            color: inherit;
            text-align: left;
            cursor: pointer;
          }

          .nav-item.hint {
            margin-top: 4px;
            margin-bottom: 8px;
            font-size: 12px;
            font-weight: 600;
            color: #b9c7ea;
            background: rgba(255, 255, 255, 0.06);
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
            padding: 12px;
            box-shadow: var(--shadow);
          }

          .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
          }

          .card {
            background: var(--card);
            border-radius: 14px;
            padding: 12px 13px;
            box-shadow: var(--shadow);
            animation: lift 0.45s ease forwards;
            transform: translateY(8px);
            opacity: 0;
          }

          .card-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
          }

          .model-id {
            display: flex;
            align-items: center;
            gap: 12px;
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
            font-size: 16px;
            line-height: 1.1;
          }

          .model-sub {
            margin: 4px 0 0;
            font-size: 12px;
            color: var(--muted);
          }

          .state {
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 12px;
            font-weight: 700;
            color: #fff;
            display: inline-flex;
            align-items: center;
            gap: 7px;
          }

          .state.online { background: #16a36d; }
          .state.wait { background: #8a95ad; }
          .state.updated { background: #6a79ff; }

          .metric {
            margin-top: 11px;
            font-size: 34px;
            font-weight: 700;
            line-height: 1;
          }

          .metric.blue { color: var(--blue); }
          .metric.green { color: var(--green); }
          .metric.purple { color: var(--purple); }
          .metric.orange { color: var(--orange); }

          .tag {
            display: inline-block;
            margin-top: 7px;
            font-size: 12px;
            font-weight: 700;
            border-radius: 999px;
            padding: 5px 10px;
            color: #fff;
            display: inline-flex;
            align-items: center;
            gap: 8px;
          }

          .tag.good { background: #16a36d; }
          .tag.pending { background: #8a95ad; }

          .panel {
            background: #fff;
            border-radius: 14px;
            box-shadow: var(--shadow);
            padding: 13px;
          }

          .actions {
            margin-top: 12px;
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 9px;
            align-items: stretch;
          }

          .action {
            border: 0;
            border-radius: 12px;
            color: #fff;
            text-align: left;
            padding: 12px 14px;
            min-height: 78px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 3px;
            cursor: pointer;
            transition: transform 0.12s ease, filter 0.12s ease;
          }

          .action:hover { transform: translateY(-1px); filter: brightness(1.05); }
          .action:disabled { opacity: 0.8; cursor: wait; }
          .action-title { font-size: 15px; font-weight: 700; line-height: 1.25; }
          .action-sub { margin-top: 2px; font-size: 12px; opacity: 0.92; line-height: 1.25; }
          .action-title i { margin-right: 10px; }

          .a1 { background: linear-gradient(90deg, #2f66ff, #2658dd); }
          .a2 { background: linear-gradient(90deg, #14a263, #0f8250); }
          .a3 { background: linear-gradient(90deg, #f28a1b, #d36f12); }
          .a4 { background: linear-gradient(90deg, #7a39d8, #632abf); }
          .a5 { background: linear-gradient(90deg, #3f4d68, #2b354b); }

          .row {
            margin-top: 12px;
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 10px;
          }

          .panel-title {
            margin: 0 0 12px;
            font-size: 18px;
          }

          .chart {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            align-items: end;
            gap: 10px;
            min-height: 230px;
            padding: 10px 9px;
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
            padding-left: 15px;
          }

          .step {
            position: relative;
            margin-bottom: 12px;
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
          .step.pending::before { background: #8ea0be; }

          .step-title {
            font-size: 14px;
            font-weight: 700;
            color: #223154;
            display: inline-flex;
            align-items: center;
            gap: 9px;
          }

          .step-sub {
            margin-top: 3px;
            font-size: 12px;
            color: #66748f;
          }

          .workflow-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 10px;
          }

          .workflow-chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
            color: #fff;
          }

          .workflow-chip.good { background: #10a86d; }
          .workflow-chip.warn { background: #c38218; }
          .workflow-chip.bad { background: #e35151; }
          .workflow-chip.processing { background: #4465d8; }

          .progress-wrap {
            margin-bottom: 12px;
            border-radius: 10px;
            overflow: hidden;
            background: #e8eefb;
            border: 1px solid #d6e0f4;
          }

          .progress-bar {
            height: 12px;
            width: 0;
            background: linear-gradient(90deg, #2f66ff, #10a86d);
            transition: width 0.35s ease;
          }

          .progress-bar.indeterminate {
            width: 45%;
            animation: flow 1.1s ease-in-out infinite;
          }

          .progress-meta {
            margin: 2px 0 10px;
            font-size: 12px;
            color: #5f6f8d;
            display: flex;
            justify-content: space-between;
            gap: 8px;
          }

          .model-state-list {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 8px;
            margin-bottom: 12px;
            background: #f8faff;
          }

          .model-state-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            padding: 7px 8px;
            border-bottom: 1px solid #e4ebf8;
            font-size: 13px;
            color: #27375a;
          }

          .model-state-item:last-child {
            border-bottom: 0;
          }

          .model-state-badge {
            border-radius: 999px;
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 700;
            color: #fff;
            min-width: 76px;
            text-align: center;
          }

          .model-state-badge.ready { background: #10a86d; }
          .model-state-badge.pending { background: #8a95ad; }
          .model-state-badge.offline { background: #e35151; }
          .model-state-badge.processing { background: #4465d8; }

          .log {
            margin-top: 12px;
            background: #0f182d;
            color: #d9e9ff;
            border-radius: 12px;
            padding: 11px;
            font: 12px/1.45 Consolas, monospace;
            height: 148px;
            overflow: auto;
          }

          .log-line.info { color: #d9e9ff; }
          .log-line.success { color: #8cf5c9; }
          .log-line.warn { color: #ffd28f; }
          .log-line.error { color: #ff9898; }

          .footer {
            margin-top: 10px;
            font-size: 12px;
            color: #6f7d96;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
          }

          @keyframes lift {
            to {
              transform: translateY(0);
              opacity: 1;
            }
          }

          @keyframes flow {
            0% { transform: translateX(-90%); }
            100% { transform: translateX(230%); }
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
            .action { min-height: 74px; }
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
            <div class="group-title">Hospital Dashboards</div>
            <button class="nav-item nav-button" onclick="openHospitalDashboard(1)"><span class="nav-icon"><i class="fa-solid fa-hospital"></i></span>Hospital-1 Dashboard</button>
            <button class="nav-item nav-button" onclick="openHospitalDashboard(2)"><span class="nav-icon"><i class="fa-solid fa-hospital-user"></i></span>Hospital-2 Dashboard</button>
            <div class="nav-item hint"><span class="nav-icon"><i class="fa-solid fa-circle-info"></i></span>Placeholder links for separate hospital UI pages.</div>
            <div class="group-title">System</div>
            <div class="nav-item"><span class="nav-icon"><i class="fa-solid fa-server"></i></span>API Status</div>
            <button class="nav-item nav-button" onclick="placeholderAction('view-logs')"><span class="nav-icon"><i class="fa-solid fa-scroll"></i></span>Logs</button>
            <button class="nav-item nav-button" onclick="placeholderAction('alerts')"><span class="nav-icon"><i class="fa-solid fa-bell"></i></span>Alert Center</button>
            <button class="nav-item nav-button" onclick="placeholderAction('exports')"><span class="nav-icon"><i class="fa-solid fa-file-export"></i></span>Export Reports</button>
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
                <div class="workflow-head">
                  <div id="workflowChip" class="workflow-chip warn"><i class="fa-solid fa-circle-notch"></i>Checking Status</div>
                </div>
                <div class="progress-wrap">
                  <div id="workflowProgressBar" class="progress-bar"></div>
                </div>
                <div class="progress-meta">
                  <span id="workflowDetail">Waiting for first status sync...</span>
                  <strong id="workflowProgressText">0%</strong>
                </div>
                <div class="model-state-list">
                  <div class="model-state-item"><span>Main model</span><span id="modelStateMain" class="model-state-badge pending">pending</span></div>
                  <div class="model-state-item"><span>Hospital-1 local model</span><span id="modelStateH1" class="model-state-badge pending">pending</span></div>
                  <div class="model-state-item"><span>Hospital-2 local model</span><span id="modelStateH2" class="model-state-badge pending">pending</span></div>
                  <div class="model-state-item"><span>Global model v2</span><span id="modelStateGlobal" class="model-state-badge pending">pending</span></div>
                </div>
                <div class="timeline">
                  <div id="stepMain" class="step pending"><div class="step-title"><i class="fa-solid fa-brain"></i>Main Model Trained</div><div class="step-sub">Random Forest on Set-1</div></div>
                  <div id="stepDeploy" class="step pending"><div class="step-title"><i class="fa-solid fa-paper-plane"></i>Model Deployed</div><div class="step-sub">Ready for remote retraining</div></div>
                  <div id="stepH1" class="step pending"><div class="step-title"><i class="fa-solid fa-hospital"></i>Hospital-1 Online</div><div class="step-sub">Service + local model endpoint</div></div>
                  <div id="stepH2" class="step pending"><div class="step-title"><i class="fa-solid fa-hospital-user"></i>Hospital-2 Online</div><div class="step-sub">Service + local model endpoint</div></div>
                  <div id="stepGlobal" class="step pending"><div class="step-title"><i class="fa-solid fa-earth-americas"></i>Aggregation Complete</div><div class="step-sub">Global model v2 generated</div></div>
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
          const workflowChip = document.getElementById('workflowChip');
          const workflowDetail = document.getElementById('workflowDetail');
          const workflowProgressText = document.getElementById('workflowProgressText');
          const workflowProgressBar = document.getElementById('workflowProgressBar');
          let isActionInFlight = false;
          let lastSnapshot = null;

          function writeLog(message, kind = 'info') {
            const stamp = new Date().toLocaleTimeString();
            logEl.innerHTML = `<div class="log-line ${kind}">[${stamp}] ${message}</div>` + logEl.innerHTML;
            document.getElementById('lastUpdated').textContent = `Last updated: ${stamp}`;
          }

          function openHospitalDashboard(hospital) {
            const path = hospital === 1 ? 'http://localhost:8001/' : 'http://localhost:8002/';
            window.open(path, '_blank', 'noopener,noreferrer');
            writeLog(`Opened placeholder for Hospital-${hospital} dashboard: ${path}`, 'info');
          }

          function placeholderAction(action) {
            const titles = {
              'view-logs': 'Logs panel placeholder clicked.',
              alerts: 'Alert center placeholder clicked.',
              exports: 'Export reports placeholder clicked.',
            };
            writeLog(titles[action] || `Placeholder clicked: ${action}`, 'warn');
          }

          function setWorkflowState(text, kind, progress, detail, indeterminate = false) {
            const iconByKind = {
              good: 'fa-circle-check',
              warn: 'fa-triangle-exclamation',
              bad: 'fa-circle-xmark',
              processing: 'fa-gear',
            };
            const clamped = Math.max(0, Math.min(100, progress));
            workflowChip.className = `workflow-chip ${kind}`;
            workflowChip.innerHTML = `<i class="fa-solid ${iconByKind[kind] || 'fa-circle-info'}"></i>${text}`;
            workflowDetail.textContent = detail;
            workflowProgressText.textContent = `${Math.round(clamped)}%`;
            if (indeterminate) {
              workflowProgressBar.className = 'progress-bar indeterminate';
            } else {
              workflowProgressBar.className = 'progress-bar';
              workflowProgressBar.style.width = `${clamped}%`;
            }
          }

          function setStep(id, state) {
            const node = document.getElementById(id);
            node.className = `step ${state}`;
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

          function setModelState(id, text, kind) {
            const node = document.getElementById(id);
            node.textContent = text;
            node.className = `model-state-badge ${kind}`;
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

          function actionText(action) {
            if (action === 'train') return 'Training main model';
            if (action === 'deploy') return 'Deploying model to hospitals';
            if (action === 'retrain-hospitals') return 'Triggering remote retraining';
            if (action === 'aggregate') return 'Aggregating local models';
            if (action === 'evaluate') return 'Evaluating global model';
            return 'Processing action';
          }

          function updateWorkflowFromStatus(status) {
            const h1 = status.hospitals?.hospital_1?.online === true;
            const h2 = status.hospitals?.hospital_2?.online === true;
            const mainReady = status.models?.base_model?.exists === true;
            const globalReady = status.models?.global_model?.exists === true;
            const cmp = status.comparison || {};
            const localModelH1 = cmp.hospital_1 !== null && cmp.hospital_1 !== undefined;
            const localModelH2 = cmp.hospital_2 !== null && cmp.hospital_2 !== undefined;

            setStep('stepMain', mainReady ? 'ok' : 'pending');
            setStep('stepDeploy', mainReady && h1 && h2 ? 'ok' : (mainReady ? 'pending' : 'bad'));
            setStep('stepH1', h1 ? 'ok' : 'bad');
            setStep('stepH2', h2 ? 'ok' : 'bad');
            setStep('stepGlobal', globalReady ? 'ok' : 'pending');

            setModelState('modelStateMain', mainReady ? 'ready' : 'pending', mainReady ? 'ready' : 'pending');
            setModelState('modelStateH1', h1 ? (localModelH1 ? 'ready' : 'pending') : 'offline', h1 ? (localModelH1 ? 'ready' : 'pending') : 'offline');
            setModelState('modelStateH2', h2 ? (localModelH2 ? 'ready' : 'pending') : 'offline', h2 ? (localModelH2 ? 'ready' : 'pending') : 'offline');
            setModelState('modelStateGlobal', globalReady ? 'ready' : 'pending', globalReady ? 'ready' : 'pending');

            const completed = [mainReady, mainReady && h1 && h2, h1, h2, globalReady].filter(Boolean).length;
            const progress = completed * 20;

            if (isActionInFlight) {
              setWorkflowState('Workflow Processing', 'processing', Math.max(progress, 35), 'Action is currently running...', true);
            } else if (!h1 && !h2) {
              setWorkflowState('Offline Services', 'bad', progress, 'Both hospitals are offline. Start hospital services first.');
            } else if (!h1 || !h2) {
              setWorkflowState('Partial Connectivity', 'warn', progress, 'One hospital is offline. Workflow is degraded.');
            } else if (globalReady) {
              setWorkflowState('Workflow Healthy', 'good', 100, 'Main, local, and global models are available.');
            } else if (mainReady) {
              setWorkflowState('Ready To Aggregate', 'warn', Math.max(progress, 40), 'Main model exists. Continue with retrain and aggregation.');
            } else {
              setWorkflowState('Waiting For Training', 'warn', Math.max(progress, 10), 'Train the main model to start federation.');
            }
          }

          async function refreshStatus() {
            try {
              const status = await fetch('/status').then((r) => r.json());
              const h1 = status.hospitals?.hospital_1?.online === true;
              const h2 = status.hospitals?.hospital_2?.online === true;
              const mainReady = status.models?.base_model?.exists === true;
              const globalReady = status.models?.global_model?.exists === true;
              const cmp = status.comparison || {};
              const localModelH1 = cmp.hospital_1 !== null && cmp.hospital_1 !== undefined;
              const localModelH2 = cmp.hospital_2 !== null && cmp.hospital_2 !== undefined;

              const mainPct = toPercent(cmp.main);
              const h1Pct = toPercent(cmp.hospital_1);
              const h2Pct = toPercent(cmp.hospital_2);
              const globalPct = toPercent(cmp.global);

              document.getElementById('mainAcc').textContent = mainPct ? `${mainPct}%` : '-';
              document.getElementById('h1Acc').textContent = h1Pct ? `${h1Pct}%` : '-';
              document.getElementById('h2Acc').textContent = h2Pct ? `${h2Pct}%` : '-';
              document.getElementById('globalAcc').textContent = globalPct ? `${globalPct}%` : '-';

              setTag('mainTag', mainReady ? 'Trained' : 'Pending', mainReady);
              setTag('h1Tag', localModelH1 ? 'Updated' : 'Outdated', localModelH1);
              setTag('h2Tag', localModelH2 ? 'Updated' : 'Outdated', localModelH2);
              setTag('globalTag', globalReady ? 'Aggregated' : 'Pending', globalReady);

              setState('h1State', h1 ? 'online' : 'offline', h1 ? 'online' : 'wait');
              setState('h2State', h2 ? 'online' : 'offline', h2 ? 'online' : 'wait');

              updateWorkflowFromStatus(status);

              const systemBadge = document.getElementById('systemBadge');
              systemBadge.innerHTML = h1 && h2
                ? '<i class="fa-solid fa-circle-check"></i>System Online'
                : '<i class="fa-solid fa-triangle-exclamation"></i>Partial Connectivity';

              if (lastSnapshot) {
                const h1Changed = lastSnapshot.h1 !== h1;
                const h2Changed = lastSnapshot.h2 !== h2;
                const globalChanged = lastSnapshot.globalReady !== globalReady;
                const mainChanged = lastSnapshot.mainReady !== mainReady;
                if (h1Changed) writeLog(`Hospital-1 is now ${h1 ? 'online' : 'offline'}.`, h1 ? 'success' : 'error');
                if (h2Changed) writeLog(`Hospital-2 is now ${h2 ? 'online' : 'offline'}.`, h2 ? 'success' : 'error');
                if (mainChanged) writeLog(`Main model status changed to ${mainReady ? 'ready' : 'missing'}.`, mainReady ? 'success' : 'warn');
                if (globalChanged) writeLog(`Global model status changed to ${globalReady ? 'ready' : 'pending'}.`, globalReady ? 'success' : 'warn');
              }
              lastSnapshot = { h1, h2, mainReady, globalReady };

              renderBars(
                mainPct ? Number(mainPct) : null,
                h1Pct ? Number(h1Pct) : null,
                h2Pct ? Number(h2Pct) : null,
                globalPct ? Number(globalPct) : null,
              );
            } catch (error) {
              setWorkflowState('Status Fetch Failed', 'bad', 0, 'Unable to reach status endpoint.');
              writeLog(`Status refresh failed: ${error}`, 'error');
            }
          }

          async function runAction(action) {
            try {
              isActionInFlight = true;
              setButtonsBusy(true);
              setWorkflowState('Workflow Processing', 'processing', 35, `${actionText(action)}...`, true);
              writeLog(`Action started: ${actionText(action)}.`, 'info');
              const endpoint = endpointFor(action);
              const res = await fetch(endpoint.path, { method: endpoint.method });
              const body = await res.json();
              if (!res.ok) {
                throw new Error(body.detail || JSON.stringify(body));
              }
              writeLog(`${action.toUpperCase()} success: ${JSON.stringify(body)}`, 'success');
              await refreshStatus();
            } catch (error) {
              setWorkflowState('Workflow Error', 'bad', 20, `Action failed while ${actionText(action).toLowerCase()}.`);
              writeLog(`${action.toUpperCase()} failed: ${error}`, 'error');
            } finally {
              isActionInFlight = false;
              setButtonsBusy(false);
              await refreshStatus();
            }
          }

          writeLog('Dashboard initialized. Waiting for system status...', 'info');
          refreshStatus();
          setInterval(refreshStatus, 15000);
        </script>
      </body>
    </html>
    """
