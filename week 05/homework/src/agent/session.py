
import logfire

def run_session(agent, prompt):
    messages = []
    
    while True:
        result = agent.run_sync(prompt, message_history=messages)
        print("\n" + result.output)
        messages = result.all_messages()
        
        answer = input("\nYou: ")
        if not answer or answer.lower() == 'stop':
            break
        prompt = answer
    
    return messages

def run_session_grouped(agent, prompt):
    with logfire.span('trivia_session'):
        return run_session(agent, prompt)
