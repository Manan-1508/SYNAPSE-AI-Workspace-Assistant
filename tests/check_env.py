import sys

def main():
    print("=== SYNAPSE Environment Verification ===")
    print(f"Running Python Version: {sys.version}")
    
    # Verify Python version requirement (3.10+)
    if sys.version_info < (3, 10):
        print("[-] Error: Python 3.10 or higher is required.")
        sys.exit(1)
        
    print("[+] Python version check passed.")
    print("=== Environment Ready ===")

if __name__ == "__main__":
    main()
