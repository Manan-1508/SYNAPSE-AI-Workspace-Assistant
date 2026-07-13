import os
import sys
import json
from unittest.mock import MagicMock, patch

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.llm.gemini import GeminiClient
from src.backend.llm.ollama import OllamaClient

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

    # 2. Test OllamaClient response generation
    print("\n=== Testing OllamaClient ===")
    mock_post_res = MagicMock()
    mock_post_res.status_code = 200
    mock_post_res.json.return_value = {"response": "Hi! I am a simulated response from Ollama."}
    
    with patch("httpx.post", return_value=mock_post_res) as mock_post:
        client = OllamaClient(temperature=0.6, max_tokens=150)
        output = client.generate_response(
            prompt="Hello local model", 
            system_instruction="Be helpful."
        )
        print(f"Mock Ollama Response output: {output}")
        assert output == "Hi! I am a simulated response from Ollama."
        
        # Verify call payload
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:1.5b",
                "prompt": "Hello local model",
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 150
                },
                "system": "Be helpful."
            },
            timeout=60.0
        )

    # 3. Test OllamaClient streaming tokens
    print("\nTesting OllamaClient streaming tokens...")
    mock_stream_context = MagicMock()
    mock_stream_res = MagicMock()
    mock_stream_res.iter_lines.return_value = [
        b'{"response": "Tok", "done": false}',
        b'{"response": "en", "done": false}',
        b'{"response": "s", "done": true}'
    ]
    mock_stream_context.__enter__.return_value = mock_stream_res
    
    with patch("httpx.stream", return_value=mock_stream_context) as mock_stream:
        client = OllamaClient()
        stream_generator = client.generate_stream("stream prompts")
        tokens = list(stream_generator)
        print(f"Streamed tokens output: {tokens}")
        assert tokens == ["Tok", "en", "s"]
        
        # Verify stream payload
        mock_stream.assert_called_once_with(
            "POST",
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:1.5b",
                "prompt": "stream prompts",
                "stream": True,
                "options": {
                    "temperature": 0.7
                }
            },
            timeout=60.0
        )

    print("[+] OllamaClient unit tests executed successfully.")

if __name__ == "__main__":
    main()
