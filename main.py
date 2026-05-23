
import sys 
from src.config import get_config 
from src.memory import ConversationMemory
from src.client import ChatClient 
from src.profile import load_profile, inject_into_system_prompt
from src import ui 

def run_chatbot():
    """Main loop - loads config, then runs conversation until exit.""" 
    
    # Step1: Load config
    # will raise ValueError with a helpful message if API key is missing
    try:
        config = get_config()
        
    except ValueError as e:
        ui.show_error(str(e))
        sya.exit(1)
        
    
    # Step 2: Create components 
    memory = ConversationMemory()  # starts empty 
    client = ChatClient(config)   # connects to Anthropic 
    
    #  Show who the profile is for
    profile = load_profile()
    if profile.get("name"):
        ui.sho_info(f"Profile loaded for: {profile['name']}")
                
    else:
        ui.show_info("No profile found - edit user_profile.json to personalize.")
    
    config["system_prompt"] = inject_into_system_prompt(config["system_prompt"])
     
    memory = ConversationMemory()
    client = ChatClient(config) 
    
    # Load previous session 
    loaded = memory.load()
    if loaded > 0: 
        ui.show_info(f"Resumed previous session - {loaded} message loaded.") 
    else: 
        ui.show_info("Starting a new session.")
        
        
    # Step 3:Show welcome screen 
    ui.show_welcome(config["model"], config["system_prompt"])
    
    # Step 4: Main conversation loop 
    while True:
        # Get user input
        user_input = ui.get_user_input()
        
        # Handle empty input 
        if not user_input:
            continue 
        
        # Handle special commands
        if user_input.lower() in ("quit", "exit", "bye"):
            memory.save()
            ui.show_info("Chat history saved.")
            ui.show_goodbye()
            break 
        
        if user_input.lower() == "clear":
            memory.clear()
            memory.save()
            ui.show_info(f"Memory cleared and history file wiped.")
            continue 
        
        if user_input.lower() == "history":
            count = memory.message_count()
            ui.show_info(f"{count} messages in memory this session.")
            
            continue 
        
        if user_input.lower() == "save":
            memory.save()
            ui.show_info("Chat history saved manually.")
            continue 
        
        if user_input.lower() == "profile": 
            p = load_profile()
            if p:
                ui.show_info(f"Name: {p.get('name')} | Working on: {p.get('currently_working_on')}")
            else:
                ui.show_info("No profile loaded.")
                
            continue 
        
        
        # The core Turn
        # 1. Add user message to memory FIRST 
        memory.add_user_message(user_input)
        
        # 2. Send full history to API , get streamng reply 
        try: 
            reply = ui.show_assistant_streaming(client, memory)
        except Exception as e:
            # Remove the user message we just added 
            memory._messages.pop()
            import traceback
            traceback.print_exc()
            ui.show_error(f"API error: {e}")
            continue 
        
        # 3. Save assistant reply to memory 
        memory.add_assistant_message(reply) 
        
        memory.save()
        

if __name__ == "__main__":
    run_chatbot()
