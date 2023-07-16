import os
import subprocess

if __name__ == "__main__":
    process = subprocess.Popen(["python", "-m", "src.cli", "start_bot"])

    for module in os.listdir("src/app/plugins"):
        if f"{module}.json" in os.listdir("data/plugins_configs"):
            process = subprocess.Popen(["powershell", "cd", f"src/app/plugins/{module}; python", f"flask_app.py"])
