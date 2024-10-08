from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from routers import (competitions_router, formations_router, nationalities_router, players_router,
                     ratings_router, squad_players_router, squads_router, team_competitions_router, team_router, users_router)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Permite solicitudes desde tu frontend local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes desde los orígenes definidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

#Routers
app.include_router(competitions_router.router)
app.include_router(formations_router.router)
app.include_router(nationalities_router.router)
app.include_router(players_router.router)
app.include_router(ratings_router.router)
app.include_router(squad_players_router.router)
app.include_router(squads_router.router)
app.include_router(team_competitions_router.router)
app.include_router(team_router.router)
app.include_router(users_router.router)

@app.get("/")
async def root():
    return "The FastAPI is running. For more info go to Help (http://127.0.0.1:8000/help)"

@app.get("/url/")
async def root():
    return "https://github.com/JorgeSP00"


@app.get("/help/")
async def root():
    return "https://github.com/JorgeSP00"
