import subprocess
import os

# Command 1: Execute npm start in the "Monitor TP" directory
subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\Users\\gamer\\OneDrive\\Documents\\tourism-management-API\\Monitor TP && npm run start'], shell=True)

# Command 2: Execute uvicorn in the "FastAPI" directory
subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\Users\\gamer\\OneDrive\\Documents\\tourism-management-API\\Hotel-API\\FastAPI && python run.py'], shell=True)

# Command 3: Execute python app.py in the "Flight-API" directory
subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\Users\\gamer\\OneDrive\\Documents\\tourism-management-API\\Flight-API && python app.py'], shell=True)

# Command 4: Execute node . in the "CLI" directory
subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'cd /d C:\\Users\\gamer\\OneDrive\\Documents\\tourism-management-API\\CLI && node .'], shell=True)
