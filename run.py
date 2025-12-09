import subprocess
import os
import sys
import time

# 1. DEFINE PATHS
# Get the absolute path of the current directory to avoid path issues
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def start_processes():
    processes = []
    
    print("🚀 Starting Project...")

    try:
        # 2. START BACKEND (FastAPI)
        # We use sys.executable to ensure it uses the same Python/Venv as this script
        print(f"🐍 Launching FastAPI from: {BACKEND_DIR}")
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
            cwd=BACKEND_DIR,  # Run command inside the backend folder
            shell=False
        )
        processes.append(backend_process)

        # 3. START FRONTEND (React)
        print(f"⚛️  Launching React from: {FRONTEND_DIR}")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=FRONTEND_DIR, # Run command inside the frontend folder
            shell=False
        )
        processes.append(frontend_process)

        # 4. MONITOR
        # Keep the script running so we can catch Ctrl+C
        print("\n✅ Both servers are running. Press Ctrl+C to stop.\n")
        
        # We wait for the processes. If one crashes, the script continues to wait for the other.
        # Alternatively, we loop to check if they are still alive.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # 5. CLEANUP
        print("\n🛑 Stopping servers...")
        for p in processes:
            p.terminate() # Sends a signal to stop the process
        print("Done.")

if __name__ == "__main__":
    start_processes()