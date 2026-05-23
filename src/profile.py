import json
import os 

PROFILE_FILE = "user_profile.json"

def load_profile(filename: str = PROFILE_FILE) -> dict:
    """ 
    Load user_profile.json.
    Returns empty dict if file doesn't exist - chatbot still works.
    """ 
    if not os.path.exists(filename):
        return {}
    
    try: 
        with open(filepath, "r", encoding="utf-8") as f: 
             return json.load(f)

    except (json.JSONDecodeError, IDError):
        return {}
    
def build_context(profile: dict) -> str:
    """
    Convert the profile dit into a clean text block for the system prompt.
    Only includes fields that are actually filled in.
    """
    
    if not profile:
        return "" 
    
    lines = ["\n---\nUSER PROFILE (always keep this in mind):"]
    
    if profile.get("name"):
        lines.append(f"Name: {profile['name']}")
        
    if profile.get("role"):
        lines.append(f"Role: {profile['role']}")
        
    if profile.get("currently_working_on"):
        lines.append(f"Currently working on: {profile['currently_working_on']}")
        
    if profile.get("goals"):
        goals =  ", ".join(profile["goals"])
        lines.append(f"Goals: {goals}") 
        
    if profile.get("skills"):
        skills = ", ".join(profile["skills"])
        lines.append(f"Current skills: {skills}")
        
    if profile.get("learning"):
        learning = ", ".join(profile["learning"])
        lines.append(f"Currently learning: {learning}") 
        
    if profile.get("Context"):
        lines.append(f"Context: {profile['context']}")
        
    prefs = profile.get("preferances", {})
    if prefs.get("response_style"):
        lines.append(f"Response style preferance: {prefs['response_style']}")
         
    if prefs.get("code_language"):
        lines.append(f"Preferred code language: {prefs['code_language']}")
        
    lines.append("---")
    return "\n".join(lines)

def inject_into_system_prompt(base_prompt: str, filepath: str = PROFILE_FILE) -> str:
    
    profile = load_profile(filepath)
    context = build_context(profile)
    return base_prompt + context 
    