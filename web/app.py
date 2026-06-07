"""
美团活动规划Agent - Web Flask 后端
提供 REST API 供前端调用
"""
import sys
import os
import json
import time
import logging
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from agent import IntentParser, ActivityPlanner, PlanExecutor
from config import LLM_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

_project_root = Path(__file__).parent.parent
_user_data_file = _project_root / "user_data.json"
_config_local_file = _project_root / "config_local.json"

# 简易速率限制：每个 IP 每分钟最多 20 次请求
_rate_limit = defaultdict(list)
RATE_LIMIT_MAX = 20
RATE_LIMIT_WINDOW = 60


def _check_rate_limit():
    ip = request.remote_addr or "unknown"
    now = time.time()
    _rate_limit[ip] = [t for t in _rate_limit[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(_rate_limit[ip]) >= RATE_LIMIT_MAX:
        return False
    _rate_limit[ip].append(now)
    return True


def _load_user_info() -> dict:
    if _user_data_file.exists():
        try:
            return json.loads(_user_data_file.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_user_info(data: dict):
    _user_data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def _save_config_local(data: dict):
    _config_local_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# 初始化组件
intent_parser = IntentParser()
planner = ActivityPlanner()
executor = PlanExecutor()

# LLM Agent（仅在配置了 API Key 时启用）
llm_agent = None
if LLM_API_KEY:
    from agent import LLMAgent
    llm_agent = LLMAgent()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """LLM 对话接口"""
    if not llm_agent:
        return jsonify({'error': '未配置 LLM_API_KEY，请设置环境变量'}), 503

    if not _check_rate_limit():
        return jsonify({'error': '请求过于频繁，请稍后再试'}), 429

    data = request.get_json()
    messages = data.get('messages', [])
    if not messages:
        return jsonify({'error': '消息不能为空'}), 400

    try:
        user_info = _load_user_info()
        user_context = None
        if user_info.get('nickname') or user_info.get('address'):
            parts = []
            if user_info.get('nickname'):
                parts.append(f"昵称={user_info['nickname']}")
            if user_info.get('address'):
                parts.append(f"常用出发地={user_info['address']}")
            if user_info.get('phone'):
                parts.append(f"手机号={user_info['phone']}")
            user_context = "用户信息：" + ", ".join(parts)

        result = llm_agent.chat(messages, user_context=user_context)
        return jsonify(result)
    except Exception as e:
        logger.exception("Chat API error")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def status():
    """检查 LLM 是否可用"""
    return jsonify({'llm_enabled': llm_agent is not None})


@app.route('/api/userinfo', methods=['GET', 'POST'])
def userinfo():
    """获取/保存用户信息"""
    if request.method == 'GET':
        return jsonify(_load_user_info())

    data = request.get_json()
    info = _load_user_info()
    if data.get('nickname') is not None:
        info['nickname'] = data['nickname']
    if data.get('phone') is not None:
        info['phone'] = data['phone']
    if data.get('address') is not None:
        info['address'] = data['address']
    _save_user_info(info)
    return jsonify({'success': True})


@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """获取/设置 LLM 配置"""
    global llm_agent
    import config as cfg

    if request.method == 'GET':
        return jsonify({
            'base_url': cfg.LLM_BASE_URL,
            'model': cfg.LLM_MODEL,
            'has_key': bool(cfg.LLM_API_KEY)
        })

    data = request.get_json()
    if data.get('base_url'):
        cfg.LLM_BASE_URL = data['base_url']
    if data.get('api_key'):
        cfg.LLM_API_KEY = data['api_key']
    if data.get('model'):
        cfg.LLM_MODEL = data['model']

    # 持久化到 config_local.json
    _save_config_local({
        'base_url': cfg.LLM_BASE_URL,
        'api_key': cfg.LLM_API_KEY,
        'model': cfg.LLM_MODEL
    })

    if cfg.LLM_API_KEY:
        from agent import LLMAgent
        llm_agent = LLMAgent()
    else:
        llm_agent = None

    return jsonify({'success': True, 'llm_enabled': llm_agent is not None})


@app.route('/api/parse', methods=['POST'])
def parse_intent():
    """解析用户意图"""
    data = request.get_json()
    user_input = data.get('input', '')
    
    if not user_input:
        return jsonify({'error': '请输入需求'}), 400
    
    intent = intent_parser.parse(user_input)
    
    return jsonify({
        'scene_type': intent.scene_type.value,
        'people_count': intent.people_count,
        'time_range': intent.time_range,
        'duration_hours': intent.duration_hours,
        'special_needs': intent.special_needs,
        'family_info': intent.family_info,
        'friend_info': intent.friend_info
    })


@app.route('/api/plan', methods=['POST'])
def create_plan():
    """生成活动方案"""
    data = request.get_json()
    intent_data = data.get('intent', {})
    
    # 重建意图对象
    from models.schemas import SceneType
    from agent.planner import UserIntent
    
    intent = UserIntent(
        scene_type=SceneType(intent_data.get('scene_type', 'family')),
        people_count=intent_data.get('people_count', 3),
        time_range=tuple(intent_data.get('time_range', ['14:00', '18:00'])),
        duration_hours=intent_data.get('duration_hours', 4.0),
        special_needs=intent_data.get('special_needs', []),
        family_info=intent_data.get('family_info'),
        friend_info=intent_data.get('friend_info')
    )
    
    # 生成方案（使用真实用户信息）
    user_info = _load_user_info()
    user_name = user_info.get('nickname', '小明')
    home_address = user_info.get('address')
    plan = planner.plan(intent, user_name=user_name, home_address=home_address)
    
    # 序列化方案
    return jsonify({
        'user_name': plan.user_name,
        'scene_type': plan.scene_type.value,
        'people_count': plan.people_count,
        'home_location': {
            'name': plan.home_location.name,
            'address': plan.home_location.address
        },
        'start_time': plan.start_time,
        'end_time': plan.end_time,
        'total_budget': plan.total_budget,
        'notes': plan.notes,
        'items': [
            {
                'venue_type': item.venue_type.value,
                'name': item.venue.name,
                'address': item.venue.location.address,
                'start_time': item.start_time,
                'end_time': item.end_time,
                'action': item.action,
                'price': item.venue.price_per_person if hasattr(item.venue, 'price_per_person') else item.venue.price
            }
            for item in plan.items
        ],
    })


@app.route('/api/execute', methods=['POST'])
def execute_plan():
    """执行预订（Demo 模式：使用确定性模拟结果）"""
    if not _check_rate_limit():
        return jsonify({'error': '请求过于频繁，请稍后再试'}), 429

    data = request.get_json()

    # 从请求中重建方案（简化处理）
    plan_data = data.get('plan', {})

    # Demo 模式：确定性模拟结果（非随机）
    bookings = []
    for i, item in enumerate(plan_data.get('items', [])):
        import hashlib
        item_hash = hashlib.md5(item.get('name', str(i)).encode()).hexdigest()
        success = int(item_hash[0], 16) > 4  # 基于名称的确定性结果
        booking_id = f"BK{int(item_hash[:6], 16) % 900000 + 100000}" if success else None
        bookings.append({
            'name': item['name'],
            'success': success,
            'booking_id': booking_id
        })
    
    # 生成最终消息
    message = generate_final_message(plan_data, bookings)
    
    return jsonify({
        'success': True,
        'bookings': bookings,
        'message': message
    })


def generate_final_message(plan_data, bookings):
    """生成最终发送的消息"""
    lines = [
        f"搞定了！下午 {plan_data.get('start_time', '14:00')} 出发，安排如下：",
        ""
    ]
    
    for i, item in enumerate(plan_data.get('items', []), 1):
        emoji = '🍽️' if item['venue_type'] == 'restaurant' else '🎯'
        lines.append(f"{i}. {item['start_time']} {emoji} {item['name']}")
        lines.append(f"   📍 {item['address']}")
        
        booking = next((b for b in bookings if b['name'] == item['name']), None)
        if booking and booking['success'] and booking['booking_id']:
            lines.append(f"   ✅ 已预订（{booking['booking_id']}）")
    
    lines.extend([
        "",
        f"💰 预计花费 ¥{plan_data.get('total_budget', 0)}，" +
        f"人均 ¥{plan_data.get('total_budget', 0) // plan_data.get('people_count', 1)}",
        "",
        "准时出发！🚗"
    ])
    
    return '\n'.join(lines)


if __name__ == '__main__':
    port = 5001
    print("=" * 50)
    print("美团活动规划Agent Web界面")
    print(f"访问: http://localhost:{port}")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=port)
