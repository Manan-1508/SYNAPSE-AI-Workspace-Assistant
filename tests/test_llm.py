import os
import sys
from unittest.mock import MagicMock, patch

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.llm.gemini import GeminiClient

def main():
    print("=== Testing GeminiClient LLM Client ===")
    
    # 1. Setup mock GenerativeModel and configure response
    mock_response = MagicMock()
    mock_response.text = "Hello! I am a simulated response from Gemini."
    
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    
    with patch("google.generativeai.GenerativeModel", return_value=mock_model) as mock_model_class:
        with patch.dict(os.environ, {"GEMINI_API_KEY": "mock-api-key-12345"}):
            client = GeminiClient(temperature=0.8, max_tokens=100)
            
            # Request response
            output = client.generate_response(
                prompt="Say hello", 
                system_instruction="You are a helper assistant."
            )
            
            print(f"Mock Response output: {output}")
            assert output == "Hello! I am a simulated response from Gemini."
            
            # Verify parameters passed to GenerativeModel constructor
            mock_model_class.assert_called_once_with(
                model_name="gemini-2.5-flash",
                generation_config={
                    "temperature": 0.8,
                    "max_output_tokens": 100
                },
                system_instruction="You are a helper assistant."
            )
            
    print("[+] GeminiClient unit tests executed successfully.")

if __name__ == "__main__":
    main()
