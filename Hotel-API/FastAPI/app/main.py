from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes import route
from app.database.base import verificar_tabela_reservas

app = FastAPI()
router = APIRouter()

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