from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import route, login
from app.database.base import verificar_tabela_reservas

app = FastAPI()

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

app.include_router(route.router, tags=["Rotas"])
app.include_router(login.router, tags=["Login"])
