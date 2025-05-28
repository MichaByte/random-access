from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel import select, Session
from .db import get_session, init_db
from .models import Player, World
from secrets import token_urlsafe
from argon2 import PasswordHasher

hasher = PasswordHasher()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/players/")
def create_player(player: Player, session: Session = Depends(get_session)) -> Player:
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


@app.get("/players/location")
def read_player_location(
    api_token: Annotated[str | None, Header()], session: Session = Depends(get_session)
):
    if not api_token:
        raise HTTPException(status_code=401, detail="No API token provided")
    hashed_token = hasher.hash(api_token)
    results = session.exec(select(Player).where(Player.api_token == hashed_token))
    if len(results.all()) != 1:
        raise HTTPException(status_code=500, detail="Critical error, please report this!")



@app.get("/players/")
def read_players(session: Session = Depends(get_session)) -> list[dict[str, int | str]]:
    players = [
        {
            "id": player.id,
            "username": player.in_game_name,
            "current_world_id": player.current_world_id,
            "level": player.level,
        }
        for player in list(session.exec(select(Player)).all())
    ]
    return players


@app.get("/worlds")
def read_worlds(session: Session = Depends(get_session)):
    worlds = list(session.exec(select(World)).all())
    return worlds
