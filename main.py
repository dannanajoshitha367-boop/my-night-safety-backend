import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()


def get_groq_api_key() -> Optional[str]:
    """
    Retrieve Groq API key from environment.
    
    Returns:
        API key string or None if not found
    """
    return os.getenv("GROQ_API_KEY")


def generate_guidance(situation_text: str) -> Optional[Dict]:
    """
    Call Groq API to generate safety guidance.
    
    Args:
        situation_text: Description of the night-time situation
        
    Returns:
        Dictionary with safety guidance or None if error occurs
    """
    
    api_key = get_groq_api_key()
    
    if not api_key:
        return {
            "error": "Groq API key not found. Please set the GROQ_API_KEY environment variable in your .env file."
        }
    
    # System prompt to guide the model
    system_prompt = """You are a Night-Safety Companion AI.

Analyze the user's described situation and generate structured night-time safety guidance.

Your output MUST strictly follow this JSON format:

{
  "risk_level": "",
  "immediate_actions": [],
  "dos": [],
  "donts": [],
  "emergency_checklist": [],
  "sos_template": ""
}

Rules:
- Risk level must be: "Low", "Medium", or "High".
- Immediate actions should be 3–5 short steps.
- Dos and Don'ts must be simple bullet-style sentences.
- Emergency checklist must contain quick safety checks.
- SOS template should be a single message users can copy.
- Be calm, clear, and reassuring.
- Do NOT add any text outside the JSON."""

    try:
        # Create Groq client - it automatically uses the API key from environment
        client = Groq()
        

        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": situation_text}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        response_text = message.choices[0].message.content
        
        # Parse JSON response
        try:
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse API response as JSON"
            }
                
    except Exception as e:
        error_msg = str(e)
        return {
            "error": f"API Error: {error_msg}"
        }


def format_response(response_text: str) -> Dict[str, str]:
    """
    Parse the API response into structured sections.
    
    Args:
        response_text: Raw response from the model
        
    Returns:
        Dictionary with parsed sections
    """
    sections = {
        "Risk Level": "",
        "Immediate Actions": "",
        "Dos": "",
        "Don'ts": "",
        "Emergency Checklist": "",
        "SOS Template": ""
    }
    
    current_section = None
    current_content = []
    
    for line in response_text.split("\n"):
        line = line.strip()
        
        # Check if this line is a section header
        if line.endswith(":"):
            # Save previous section
            if current_section and current_content:
                sections[current_section] = "\n".join(current_content).strip()
            
            # Start new section
            current_section = line.rstrip(":")
            current_content = []
        elif line and current_section:
            current_content.append(line)
    
    # Save the last section
    if current_section and current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections