import datetime
import logging
import os
from httpx import Request
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import route, login
from app.database.base import verificar_tabela_reservas
from app.database.session import init_db

app = FastAPI()

app.include_router(route.router, tags=["Rotas"])
app.include_router(login.router, tags=["Login"])


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

verificar_tabela_reservas()

@app.get("/", response_class=HTMLResponse, tags=["Main"])
async def read_root():
    return """
    <html>
        <head>
            <title>Welcome to Hotel Management API</title>
        </head>
        <body>
            <h1>Welcome to Hotel Management API</h1>
            <p>You can access the FastAPI documentation <a href="/docs">here</a>.</p>
        </body>
    </html>
    """

log_directory = "System_Logs"  
os.makedirs(log_directory, exist_ok=True)

# Configurar o logger para salvar em arquivos rotativos
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Define o formato da data no nome do arquivo de log
log_file_format = "%Y-%m-%d.log"

# Define o manipulador de arquivo rotativo
file_handler = logging.FileHandler(
    os.path.join(log_directory, datetime.now().strftime(log_file_format))
)

logger.addHandler(file_handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()

    response = await call_next(request)

    end_time = datetime.now()
    elapsed_time = end_time - start_time

    logger.info(
        f"{request.client} - "
        f"['{request.method} {request.url.path}'] - "
        f"{response.status_code} - "
        f"[Hora:{end_time.strftime('%H:%M:%S')}] - "
        f"[Tempo:'{elapsed_time.total_seconds():.3f}'s]"
    )

    return response

