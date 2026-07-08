import os
import sys

# Add project root directory to path to enable direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.parsers.manager import ParserManager

def main():
    print("=== Running Unified Document Parsers Verification ===")
    manager = ParserManager()
