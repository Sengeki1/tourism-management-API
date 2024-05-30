from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import aiohttp

from app.api.routes import route
from app.database.base import verificar_tabela_reservas

app = FastAPI()

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


@app.get("/external-api", tags=["External[Example]"])
async def call_external_api():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/todos/1') as response:
            data = await response.json()
            return data


app.include_router(route.router, tags=["Rotas"])
