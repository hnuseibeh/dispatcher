# demo_scenario.py

from core.a2a.dispatcher import dispatch_subtask

def simulate_agent_to_agent():
    parent_task = {
        "id": "task-001",
        "prompt": "Research and summarize the latest AI models",
        "agent": "Claude3"
    }
    subtask = {
        "prompt": "Summarize Claude 3 model architecture and use cases",
        "required_agent": "Claude3",
        "parent_task_id": "task-001"
    }

    result = dispatch_subtask(subtask)
    print("Subtask Result:", result)