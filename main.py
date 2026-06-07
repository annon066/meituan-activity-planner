#!/usr/bin/env python3
"""
美团活动规划Agent - 命令行界面
演示：接受自然语言输入，生成完整活动方案并执行预订
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')

from agent import IntentParser, ActivityPlanner, PlanExecutor
from utils import print_separator


class ActivityAgentCLI:
    """命令行交互界面"""
    
    def __init__(self):
        self.intent_parser = IntentParser()
        self.planner = ActivityPlanner()
        self.executor = PlanExecutor()
    
    def run(self):
        """运行CLI"""
        self._print_welcome()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n请描述您的需求（或输入 'quit' 退出）:\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n感谢使用，再见！")
                    break
                
                if not user_input:
                    continue
                
                # 处理请求
                self._process_request(user_input)
                
            except KeyboardInterrupt:
                print("\n\n已取消，再见！")
                break
            except Exception as e:
                print(f"\n处理出错: {e}")
    
    def _print_welcome(self):
        """打印欢迎信息"""
        print("""
╔══════════════════════════════════════════════════════════╗
║          🎯 美团活动规划 Agent                            ║
║          短时活动规划与预订助手                           ║
╚══════════════════════════════════════════════════════════╝

示例输入:
  - "今天下午是空的，想和老婆孩子出去玩几个小时，孩子5岁，老婆在减肥"
  - "周末想和4个朋友聚会，2男2女，下午有空"
  - "下午2点到6点，带家人出去玩"

命令: quit/exit 退出
""")
    
    def _process_request(self, user_input: str):
        """处理用户请求"""
        print("\n" + "=" * 60)
        print("📋 正在分析您的需求...")
        print("=" * 60)
        
        # 1. 解析意图
        intent = self.intent_parser.parse(user_input)
        self._print_intent(intent)
        
        # 2. 生成计划
        print("\n🔍 正在搜索合适的场所和活动...")
        plan = self.planner.plan(intent, user_name="小明")
        self._print_plan(plan)
        
        # 3. 询问确认
        confirm = input("\n是否确认此方案并执行预订？(y/n): ").strip().lower()
        
        if confirm == 'y':
            # 4. 执行预订
            print("\n📝 正在执行预订操作...")
            plan = self.executor.execute(plan)
            self._print_booking_result(plan)
            
            # 5. 生成最终方案
            print("\n" + "=" * 60)
            print("✅ 方案已确认！以下是为您准备的完整行程：")
            print("=" * 60)
            print(plan.to_summary())
            
            # 6. 模拟发送消息
            self._print_final_message(plan)
        else:
            print("\n已取消方案。您可以重新描述需求。")
    
    def _print_intent(self, intent):
        """打印解析结果"""
        print(f"""
✓ 场景类型: {'家庭亲子' if intent.scene_type.value == 'family' else '朋友聚会'}
✓ 人数: {intent.people_count}人
✓ 时间: {intent.time_range[0]} - {intent.time_range[1]} ({intent.duration_hours}小时)
✓ 特殊需求: {', '.join(intent.special_needs) if intent.special_needs else '无'}
""")
    
    def _print_plan(self, plan):
        """打印计划详情"""
        print(f"\n📍 出发地: {plan.home_location.name}")
        print(f"⏰ 时间段: {plan.start_time} - {plan.end_time}")
        print(f"👥 人数: {plan.people_count}人")
        print(f"💰 预计花费: ¥{plan.total_budget}")
        
        print("\n📋 活动安排:")
        for i, item in enumerate(plan.items, 1):
            emoji = "🍽️" if item.venue_type.value == "restaurant" else "🎯"
            print(f"  {i}. {emoji} {item.start_time}-{item.end_time}")
            print(f"     名称: {item.venue.name}")
            print(f"     地址: {item.venue.location.address}")
            print(f"     操作: {item.action}")
    
    def _print_booking_result(self, plan):
        """打印预订结果"""
        success = sum(1 for item in plan.items if item.status in ("booked", "confirmed"))
        total = len(plan.items)

        print(f"\n✓ 完成: {success}/{total}")

        for item in plan.items:
            if item.status == "booked" and item.booking_info:
                print(f"  ✅ {item.venue.name} - 预订成功")
                if item.booking_info.booking_id:
                    print(f"     预订号: {item.booking_info.booking_id}")
            elif item.status == "confirmed":
                print(f"  ✅ {item.venue.name} - 无需预订，直接到店")
            elif item.status == "failed":
                print(f"  ❌ {item.venue.name} - 预订失败")
    
    def _print_final_message(self, plan):
        """打印最终消息"""
        message = f"""
📨 已为您生成完整方案，可以发送给家人/朋友：

--------------------------------------------
搞定了！下午 {plan.start_time} 出发，安排如下：

"""
        for i, item in enumerate(plan.items, 1):
            emoji = "🍽️" if item.venue_type.value == "restaurant" else "🎯"
            message += f"{i}. {item.start_time} {emoji} {item.venue.name}\n"
            message += f"   📍 {item.venue.location.address}\n"
            if item.booking_info and item.booking_info.booking_id:
                message += f"   ✅ 已预订（{item.booking_info.booking_id}）\n"
        
        message += f"""
💰 预计花费 ¥{plan.total_budget}，人均 ¥{plan.total_budget // plan.people_count}

准时出发！🚗
--------------------------------------------
"""
        print(message)


def demo_scenarios():
    """演示预设场景"""
    print("\n" + "=" * 60)
    print("🎭 演示模式 - 预设场景展示")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "家庭亲子场景",
            "input": "今天下午是空的，想和老婆孩子出去玩几个小时，孩子5岁，老婆在减肥"
        },
        {
            "name": "朋友聚会场景",
            "input": "周末想和4个朋友聚会，2男2女，下午有空，别离家太远"
        }
    ]
    
    intent_parser = IntentParser()
    planner = ActivityPlanner()
    executor = PlanExecutor()
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"📌 场景: {scenario['name']}")
        print(f"💬 输入: \"{scenario['input']}\"")
        print("=" * 60)
        
        # 解析
        intent = intent_parser.parse(scenario['input'])
        
        # 规划
        plan = planner.plan(intent, user_name="小明")
        
        # 执行（模拟）
        plan = executor.execute(plan)
        
        # 输出
        print(plan.to_summary())
        
        input("\n按回车继续下一个场景...")


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='美团活动规划Agent')
    parser.add_argument('--demo', action='store_true', help='运行演示模式')
    parser.add_argument('--input', '-i', type=str, help='直接处理输入')
    args = parser.parse_args()
    
    cli = ActivityAgentCLI()
    
    if args.demo:
        demo_scenarios()
    elif args.input:
        cli._process_request(args.input)
    else:
        cli.run()


if __name__ == "__main__":
    main()
