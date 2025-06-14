# Final wrapper for prompt injection with full MCP context

def inject_context(task_description, rules, lessons):
    return {
        'context': {
            'task': task_description,
            'rules': rules,
            'memory': lessons
        }
    }
