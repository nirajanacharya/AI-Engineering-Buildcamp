"""Utility functions for agent testing"""


def collect_tools(messages):
    """Extract tool call names from agent message history
    
    Args:
        messages: List of messages from agent run
        
    Returns:
        List of tool names called in order
    """
    tool_calls = []
    for msg in messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for call in msg.tool_calls:
                tool_calls.append(call.function.name)
    return tool_calls
