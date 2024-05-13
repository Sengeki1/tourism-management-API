import subprocess

subprocess.run("cd 'Monitor TP' && npm run start", shell=True)
subprocess.run("cd Hotel-API/FastAPI && uvicorn --host=0.0.0.0 run:app --reload", shell=True)
subprocess.run("python3 app.py", shell=True)
subprocess.run("cd CLI && node.", shell=True)
