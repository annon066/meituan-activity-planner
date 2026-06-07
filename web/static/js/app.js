/**
 * 美团活动规划Agent - 前端交互逻辑
 */

// API 端点
const API = {
    parse: '/api/parse',
    plan: '/api/plan',
    execute: '/api/execute'
};

// 状态管理
let currentPlan = null;
let loadingStepIndex = 0;
let loadingInterval = null;

// DOM 元素
const elements = {
    userInput: document.getElementById('user-input'),
    submitBtn: document.getElementById('submit-btn'),
    scenarioBtns: document.querySelectorAll('.scenario-btn'),
    loadingSection: document.getElementById('loading-section'),
    intentSection: document.getElementById('intent-section'),
    planSection: document.getElementById('plan-section'),
    resultSection: document.getElementById('result-section'),
    confirmBtn: document.getElementById('confirm-btn'),
    resetBtn: document.getElementById('reset-btn'),
    copyBtn: document.getElementById('copy-btn'),
    newPlanBtn: document.getElementById('new-plan-btn'),
    loadingSteps: document.querySelectorAll('.loading-step')
};

// 场景预设文案
const scenarioPrompts = {
    family: '今天下午是空的，想和老婆孩子出去玩几个小时，孩子5岁，老婆在减肥',
    friends: '周末想和4个朋友聚会，2男2女，下午有空，别离家太远',
    couple: '下午想和女朋友约会，想找个浪漫的地方吃饭，然后看电影',
    solo: '今天下午想一个人放松一下，找个人少安静的地方看书喝咖啡'
};

// 场景类型映射
const sceneTypeMap = {
    family: '👨‍👩‍👧 家庭亲子',
    friends: '👥 朋友聚会',
    couple: '💑 情侣约会',
    solo: '🧘 独自放松'
};

// 快速场景选择
elements.scenarioBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const scene = btn.dataset.scene;
        if (scenarioPrompts[scene]) {
            elements.userInput.value = scenarioPrompts[scene];
            elements.userInput.focus();
        }
    });
});

// 提交按钮
elements.submitBtn.addEventListener('click', async () => {
    const input = elements.userInput.value.trim();
    if (!input) {
        shakeElement(elements.userInput);
        return;
    }

    await handlePlanRequest(input);
});

// 确认预订
elements.confirmBtn.addEventListener('click', async () => {
    if (currentPlan) {
        await handleExecutePlan(currentPlan);
    }
});

// 重新规划
elements.resetBtn.addEventListener('click', () => {
    resetUI();
    elements.userInput.focus();
});

// 新的规划
elements.newPlanBtn.addEventListener('click', () => {
    resetUI();
    elements.userInput.focus();
});

// 复制消息
elements.copyBtn.addEventListener('click', async () => {
    const message = document.getElementById('final-message-content').textContent;
    try {
        await navigator.clipboard.writeText(message);
        const btn = elements.copyBtn;
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<span class="copy-icon">✓</span><span>已复制</span>';
        btn.style.background = 'var(--success)';
        btn.style.color = 'white';
        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.style.background = '';
            btn.style.color = '';
        }, 2000);
    } catch (err) {
        console.error('复制失败:', err);
    }
});

// 输入框回车提交
elements.userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        elements.submitBtn.click();
    }
});

/**
 * 处理规划请求
 */
async function handlePlanRequest(input) {
    showLoading();
    startLoadingAnimation();

    try {
        // 1. 解析意图
        updateLoadingStep(0);
        const intent = await fetchAPI(API.parse, { input });
        await delay(800);

        // 2. 生成方案
        updateLoadingStep(1);
        const plan = await fetchAPI(API.plan, { intent });
        await delay(800);

        updateLoadingStep(2);
        await delay(600);

        currentPlan = plan;
        stopLoadingAnimation();
        showIntent(intent);
        showPlan(plan);
        hideLoading();

    } catch (error) {
        stopLoadingAnimation();
        hideLoading();
        showErrorToast('规划失败: ' + (error.message || '网络错误'));
    }
}

/**
 * 执行预订
 */
async function handleExecutePlan(plan) {
    showLoading();
    startLoadingAnimation();
    updateLoadingStep(0);

    try {
        // 模拟加载步骤
        await delay(800);
        updateLoadingStep(1);
        await delay(600);
        updateLoadingStep(2);
        await delay(600);

        const result = await fetchAPI(API.execute, { plan });

        stopLoadingAnimation();
        showResult(result);
        hideLoading();

    } catch (error) {
        stopLoadingAnimation();
        hideLoading();
        showErrorToast('预订失败: ' + (error.message || '网络错误'));
    }
}

/**
 * API 调用封装
 */
async function fetchAPI(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error('API 请求失败');
    }

    return response.json();
}

/**
 * 显示意图解析结果
 */
function showIntent(intent) {
    const sceneType = intent.scene_type || 'family';
    document.getElementById('scene-type').textContent =
        sceneTypeMap[sceneType] || sceneTypeMap.family;

    document.getElementById('people-count').textContent = (intent.people_count || 3) + '人';
    document.getElementById('time-range').textContent =
        `${intent.time_range[0] || '14:00'} - ${intent.time_range[1] || '18:00'}`;

    const needs = intent.special_needs || [];
    document.getElementById('special-needs').textContent =
        needs.length ? needs.join(', ') : '无特殊需求';

    elements.intentSection.classList.remove('hidden');
}

/**
 * 显示方案
 */
function showPlan(plan) {
    // 元信息
    document.getElementById('home-location').textContent =
        plan.home_location?.name || '当前位置';
    document.getElementById('total-budget').textContent = '¥' + (plan.total_budget || 0);
    document.getElementById('plan-people').textContent = (plan.people_count || 1) + '人';

    // 时间线
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = plan.items?.map((item, index) => `
        <div class="timeline-item ${item.venue_type}" style="animation-delay: ${index * 0.1}s">
            <div class="timeline-time">
                <span>🕐</span>
                <span>${item.start_time || '14:00'} - ${item.end_time || '15:30'}</span>
            </div>
            <div class="timeline-title">
                ${item.venue_type === 'restaurant' ? '🍽️' : '🎯'} ${item.name || item.venue?.name || '活动地点'}
            </div>
            <div class="timeline-address">
                <span>📍</span>
                <span>${item.address || item.venue?.location?.address || '地址未知'}</span>
            </div>
            <div class="timeline-price">
                💰 人均 ¥${item.price || 0}
            </div>
        </div>
    `).join('') || '<div class="timeline-item">暂无活动安排</div>';

    elements.planSection.classList.remove('hidden');
}

/**
 * 显示预订结果
 */
function showResult(result) {
    // 预订结果
    const bookingResults = document.getElementById('booking-results');
    bookingResults.innerHTML = result.bookings?.map(b => `
        <div class="booking-item ${b.success ? 'success' : 'failed'}">
            <div class="booking-icon">${b.success ? '✅' : '❌'}</div>
            <div class="booking-info">
                <div class="booking-name">${b.name}</div>
                ${b.booking_id ? `<div class="booking-id">预订号: ${b.booking_id}</div>` : ''}
            </div>
            <div class="booking-status">${b.success ? '预订成功' : '预订失败'}</div>
        </div>
    `).join('') || '<div class="booking-item">暂无预订信息</div>';

    // 最终消息
    document.getElementById('final-message-content').textContent = result.message || '预订完成';

    elements.planSection.classList.add('hidden');
    elements.intentSection.classList.add('hidden');
    elements.resultSection.classList.remove('hidden');
}

/**
 * 显示/隐藏加载
 */
function showLoading() {
    elements.loadingSection.classList.remove('hidden');
    elements.intentSection.classList.add('hidden');
    elements.planSection.classList.add('hidden');
    elements.resultSection.classList.add('hidden');
}

function hideLoading() {
    elements.loadingSection.classList.add('hidden');
}

/**
 * 加载动画
 */
function startLoadingAnimation() {
    loadingStepIndex = 0;
    updateLoadingStep(0);
}

function stopLoadingAnimation() {
    loadingStepIndex = 0;
}

function updateLoadingStep(index) {
    elements.loadingSteps.forEach((step, i) => {
        if (i === index) {
            step.classList.add('active');
        } else if (i < index) {
            step.classList.remove('active');
            step.style.background = 'var(--success-light)';
            step.style.color = 'var(--success)';
        } else {
            step.classList.remove('active');
            step.style.background = '';
            step.style.color = '';
        }
    });
}

/**
 * 重置UI
 */
function resetUI() {
    elements.userInput.value = '';
    elements.intentSection.classList.add('hidden');
    elements.planSection.classList.add('hidden');
    elements.resultSection.classList.add('hidden');
    elements.loadingSection.classList.add('hidden');
    currentPlan = null;
}

/**
 * 工具函数
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function shakeElement(element) {
    element.style.animation = 'none';
    element.offsetHeight; // 触发重排
    element.style.animation = 'shake 0.5s';
    setTimeout(() => {
        element.style.animation = '';
    }, 500);
}

function showErrorToast(message) {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: var(--danger);
        color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 9999;
        animation: slideInRight 0.3s;
        max-width: 300px;
    `;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// 添加震动动画
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);