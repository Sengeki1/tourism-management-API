import subprocess

subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd 'Monitor TP' && npm run start"])
subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd Hotel-API/FastAPI && uvicorn --host=0.0.0.0 run:app --reload"])
subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "python3 app.py"])
subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd CLI && node."])
