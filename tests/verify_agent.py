import sys
import os
from unittest.mock import MagicMock

# Mock google.generativeai if missing
try:
    import google.generativeai as genai
except ImportError:
    print("Warning: google.generativeai not installed. Mocking for verification.")
    genai = MagicMock()
    # Mock the chat session
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "I recommend the Paris trip because it matches your romantic interest."
    
    mock_model = MagicMock()
    mock_model.start_chat.return_value = mock_chat
    genai.GenerativeModel.return_value = mock_model
    # CRITICAL: Register in sys.modules so imports in other files work
    sys.modules["google.generativeai"] = genai
    sys.modules["google"] = MagicMock() # Ensure parent package exists if needed
    sys.modules["google.generativeai"] = genai

from agent.coordinator import run_agent

# Mock input to simulate user interaction
original_input = __builtins__.input
inputs = iter(["I want a romantic trip to Paris", "quit"])

def mock_input(prompt=None):
    try:
        return next(inputs)
    except StopIteration:
        return "quit"

try:
    __builtins__.input = mock_input
    print("Starting Agent Verification...")
    run_agent()
    print("Agent Verification Completed Successfully.")
except Exception as e:
    print(f"Agent Verification Failed: {e}")
finally:
    __builtins__.input = original_input
