#!/usr/bin/env python3
"""
美团活动规划Agent - Web UI
零依赖实现：使用 Python 标准库 http.server + 内嵌前端
运行: python3 web_ui.py
访问: http://localhost:7860
"""
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

from agent import IntentParser, ActivityPlanner, PlanExecutor
from models.schemas import VenueType

intent_parser = IntentParser()
activity_planner = ActivityPlanner()
plan_executor = PlanExecutor()

# 存储当前方案（Demo用，单用户）
plans_store = {}


HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>美团活动规划 Agent</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}
.container {
    max-width: 900px;
    margin: 0 auto;
}
.header {
    text-align: center;
    color: white;
    margin-bottom: 30px;
}
.header h1 { font-size: 2em; margin-bottom: 8px; }
.header p { opacity: 0.9; font-size: 1.1em; }
.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}
.input-section textarea {
    width: 100%;
    padding: 16px;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 16px;
    resize: vertical;
    min-height: 80px;
    transition: border-color 0.3s;
}
.input-section textarea:focus {
    outline: none;
    border-color: #667eea;
}
.examples {
    display: flex;
    gap: 10px;
    margin-top: 12px;
    flex-wrap: wrap;
}
.example-btn {
    padding: 8px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    background: #f7fafc;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}
.example-btn:hover {
    background: #edf2f7;
    border-color: #667eea;
    color: #667eea;
}
.btn-primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 14px 32px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 16px;
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.btn-confirm {
    background: linear-gradient(135deg, #48bb78, #38a169);
    color: white;
    border: none;
    padding: 14px 32px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: transform 0.2s;
}
.btn-confirm:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(72,187,120,0.4); }
.result-section { display: none; }
.result-section.visible { display: block; }
.intent-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
}
.intent-table td {
    padding: 10px 16px;
    border-bottom: 1px solid #f0f0f0;
}
.intent-table td:first-child {
    font-weight: 600;
    color: #4a5568;
    width: 100px;
}
.plan-item {
    display: flex;
    align-items: flex-start;
    padding: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin: 10px 0;
    transition: border-color 0.2s;
}
.plan-item:hover { border-color: #667eea; }
.plan-item .emoji { font-size: 2em; margin-right: 16px; }
.plan-item .info { flex: 1; }
.plan-item .info h4 { margin-bottom: 4px; color: #2d3748; }
.plan-item .info p { color: #718096; font-size: 14px; margin: 2px 0; }
.plan-item .time-badge {
    background: #edf2f7;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    color: #4a5568;
}
.budget-bar {
    display: flex;
    justify-content: space-between;
    background: #f7fafc;
    padding: 12px 20px;
    border-radius: 10px;
    margin-top: 12px;
}
.budget-bar span { color: #4a5568; }
.budget-bar .amount { font-weight: 700; color: #e53e3e; }
.booking-result {
    padding: 12px 16px;
    border-radius: 10px;
    margin: 8px 0;
    font-size: 15px;
}
.booking-success { background: #f0fff4; border: 1px solid #c6f6d5; color: #276749; }
.booking-walkin { background: #ebf8ff; border: 1px solid #bee3f8; color: #2a4365; }
.booking-failed { background: #fed7d7; border: 1px solid #feb2b2; color: #9b2c2c; }
.share-box {
    background: #1a202c;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 12px;
    font-family: monospace;
    font-size: 14px;
    white-space: pre-wrap;
    margin-top: 16px;
    position: relative;
}
.copy-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #4a5568;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
}
.copy-btn:hover { background: #667eea; }
.loading { text-align: center; padding: 20px; color: #718096; }
.loading::after {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #e2e8f0;
    border-top-color: #667eea;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-left: 10px;
    vertical-align: middle;
}
@keyframes spin { to { transform: rotate(360deg); } }
.section-title {
    font-size: 1.1em;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🎯 美团活动规划 Agent</h1>
        <p>短时活动规划与预订助手 — 输入一句话需求，自动规划方案并执行预订</p>
    </div>

    <div class="card input-section">
        <div class="section-title">💬 描述您的需求</div>
        <textarea id="userInput" placeholder="例：今天下午是空的，想和老婆孩子出去玩几个小时，孩子5岁，老婆在减肥"></textarea>
        <div class="examples">
            <button class="example-btn" onclick="setExample('family')">👨‍👩‍👧 家庭亲子场景</button>
            <button class="example-btn" onclick="setExample('friends')">👫 朋友聚会场景</button>
        </div>
        <button class="btn-primary" id="submitBtn" onclick="generatePlan()">🔍 生成方案</button>
    </div>

    <div class="card result-section" id="intentSection">
        <div class="section-title">📋 意图分析</div>
        <table class="intent-table" id="intentTable"></table>
    </div>

    <div class="card result-section" id="planSection">
        <div class="section-title">🗓️ 活动方案</div>
        <div id="planItems"></div>
        <div class="budget-bar" id="budgetBar"></div>
        <button class="btn-confirm" id="confirmBtn" onclick="confirmPlan()">✅ 确认方案并执行预订</button>
    </div>

    <div class="card result-section" id="resultSection">
        <div class="section-title">📝 预订结果</div>
        <div id="bookingResults"></div>
    </div>

    <div class="card result-section" id="shareSection">
        <div class="section-title">📨 可发送给家人/朋友的消息</div>
        <div class="share-box" id="shareBox">
            <button class="copy-btn" onclick="copyShare()">复制</button>
            <span id="shareText"></span>
        </div>
    </div>
</div>

<script>
const EXAMPLES = {
    family: '今天下午是空的，想和老婆孩子出去玩几个小时，别离家太远，孩子5岁，老婆最近在减肥',
    friends: '周末下午想和朋友出去玩几个小时，总共4个人，2个男生2个女生，别离家太远'
};

function setExample(type) {
    document.getElementById('userInput').value = EXAMPLES[type];
}

async function generatePlan() {
    const input = document.getElementById('userInput').value.trim();
    if (!input) return alert('请输入您的需求');

    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.textContent = '⏳ 正在规划...';

    // 隐藏之前的结果
    hide('intentSection'); hide('planSection'); hide('resultSection'); hide('shareSection');

    try {
        const res = await fetch('/api/plan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({input: input})
        });
        const data = await res.json();

        if (data.error) { alert(data.error); return; }

        renderIntent(data.intent);
        renderPlan(data.plan);
        show('intentSection'); show('planSection');
    } catch(e) {
        alert('请求失败: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔍 生成方案';
    }
}

async function confirmPlan() {
    const btn = document.getElementById('confirmBtn');
    btn.disabled = true;
    btn.textContent = '⏳ 正在预订...';

    try {
        const res = await fetch('/api/confirm', { method: 'POST' });
        const data = await res.json();

        if (data.error) { alert(data.error); return; }

        renderResult(data.results);
        renderShare(data.share_message);
        show('resultSection'); show('shareSection');
    } catch(e) {
        alert('请求失败: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '✅ 确认方案并执行预订';
    }
}

function renderIntent(intent) {
    const rows = [
        ['场景类型', intent.scene_type === 'family' ? '👨‍👩‍👧 家庭亲子' : '👫 朋友聚会'],
        ['人数', intent.people_count + '人'],
        ['时间段', intent.time_range[0] + ' - ' + intent.time_range[1] + '（' + intent.duration_hours + '小时）'],
        ['特殊需求', intent.special_needs.length ? intent.special_needs.join('、') : '无']
    ];
    document.getElementById('intentTable').innerHTML = rows.map(r =>
        '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'
    ).join('');
}

function renderPlan(plan) {
    const items = plan.items.map((item, i) => {
        const emoji = item.venue_type === 'restaurant' ? '🍽️' : '🎯';
        return '<div class="plan-item">' +
            '<div class="emoji">' + emoji + '</div>' +
            '<div class="info">' +
                '<h4>' + item.venue_name + '</h4>' +
                '<p>📍 ' + item.address + '</p>' +
                '<p>🎫 ' + item.action + '</p>' +
            '</div>' +
            '<div class="time-badge">' + item.start_time + '-' + item.end_time + '</div>' +
        '</div>';
    }).join('');
    document.getElementById('planItems').innerHTML = items;
    document.getElementById('budgetBar').innerHTML =
        '<span>👥 ' + plan.people_count + '人</span>' +
        '<span>⏰ ' + plan.start_time + '-' + plan.end_time + '</span>' +
        '<span class="amount">💰 ¥' + plan.total_budget + '（人均¥' + Math.floor(plan.total_budget/plan.people_count) + '）</span>';
}

function renderResult(results) {
    const html = results.map(r => {
        let cls, icon, text;
        if (r.status === 'booked') {
            cls = 'booking-success'; icon = '✅'; text = '预订成功（' + r.booking_id + '）';
        } else if (r.status === 'confirmed') {
            cls = 'booking-walkin'; icon = '✅'; text = '无需预订，直接到店';
        } else {
            cls = 'booking-failed'; icon = '❌'; text = '预订失败';
        }
        return '<div class="booking-result ' + cls + '">' + icon + ' <strong>' + r.name + '</strong> — ' + text + '</div>';
    }).join('');
    document.getElementById('bookingResults').innerHTML = html;
}

function renderShare(msg) {
    document.getElementById('shareText').textContent = msg;
}

function copyShare() {
    const text = document.getElementById('shareText').textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector('.copy-btn');
        btn.textContent = '已复制!';
        setTimeout(() => btn.textContent = '复制', 1500);
    });
}

function show(id) { document.getElementById(id).classList.add('visible'); }
function hide(id) { document.getElementById(id).classList.remove('visible'); }
</script>
</body>
</html>"""


class AgentHandler(BaseHTTPRequestHandler):
    """HTTP请求处理"""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'

        if self.path == '/api/plan':
            self._handle_plan(body)
        elif self.path == '/api/confirm':
            self._handle_confirm()
        else:
            self._json_response(404, {"error": "Not found"})

    def _handle_plan(self, body):
        """处理规划请求"""
        try:
            data = json.loads(body)
            user_input = data.get("input", "").strip()
            if not user_input:
                self._json_response(400, {"error": "请输入您的需求"})
                return

            intent = intent_parser.parse(user_input)
            plan = activity_planner.plan(intent, user_name="小明")
            plans_store["current"] = plan

            response = {
                "intent": {
                    "scene_type": intent.scene_type.value,
                    "people_count": intent.people_count,
                    "time_range": list(intent.time_range),
                    "duration_hours": intent.duration_hours,
                    "special_needs": intent.special_needs
                },
                "plan": {
                    "start_time": plan.start_time,
                    "end_time": plan.end_time,
                    "people_count": plan.people_count,
                    "total_budget": plan.total_budget,
                    "home_location": plan.home_location.name,
                    "notes": plan.notes,
                    "items": [
                        {
                            "venue_type": item.venue_type.value,
                            "venue_name": item.venue.name,
                            "address": item.venue.location.address,
                            "start_time": item.start_time,
                            "end_time": item.end_time,
                            "action": item.action
                        }
                        for item in plan.items
                    ]
                }
            }
            self._json_response(200, response)

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _handle_confirm(self):
        """处理确认预订请求"""
        try:
            plan = plans_store.get("current")
            if not plan:
                self._json_response(400, {"error": "请先生成方案"})
                return

            plan = plan_executor.execute(plan)
            plans_store["current"] = plan

            results = []
            for item in plan.items:
                r = {
                    "name": item.venue.name,
                    "status": item.status,
                    "booking_id": item.booking_info.booking_id if item.booking_info else None
                }
                results.append(r)

            share_msg = self._build_share_message(plan)

            self._json_response(200, {
                "results": results,
                "share_message": share_msg
            })

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _build_share_message(self, plan):
        """生成可分享消息"""
        lines = [f"搞定了！下午 {plan.start_time} 出发，安排如下：", ""]

        for i, item in enumerate(plan.items, 1):
            emoji = "🍽️" if item.venue_type == VenueType.RESTAURANT else "🎯"
            lines.append(f"{i}. {item.start_time} {emoji} {item.venue.name}")
            lines.append(f"   📍 {item.venue.location.address}")
            if item.booking_info and item.booking_info.booking_id:
                lines.append(f"   ✅ 已预订（{item.booking_info.booking_id}）")
            elif item.status == "confirmed":
                lines.append(f"   ✅ 直接到店")

        lines.extend([
            "",
            f"💰 预计花费 ¥{plan.total_budget}，人均 ¥{plan.total_budget // plan.people_count}",
            "",
            "准时出发！🚗"
        ])

        return "\n".join(lines)

    def _json_response(self, code, data):
        """发送JSON响应"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """简化日志"""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    port = 7860
    host = '127.0.0.1'
    try:
        server = HTTPServer((host, port), AgentHandler)
    except OSError as e:
        if 'Address already in use' in str(e):
            port = 8080
            server = HTTPServer((host, port), AgentHandler)
        else:
            raise

    print(f"""
╔══════════════════════════════════════════════════════════╗
║          🎯 美团活动规划 Agent - Web UI                  ║
╚══════════════════════════════════════════════════════════╝

  🌐 请在浏览器打开: http://127.0.0.1:{port}
  📝 按 Ctrl+C 停止服务
""")
    try:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{port}')
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()


if __name__ == "__main__":
    main()
