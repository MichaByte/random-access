import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Integer


class ItemCategory(str, Enum):
    ranged_weapon = "ranged_weapon"
    melee_weapon = "melee_weapon"
    armor_head = "armor_head"
    armor_torso = "armor_torso"
    armor_legs = "armor_legs"
    armor_shoes = "armor_shoes"
    potion = "potion"
    throwable_potion = "throwable_potion"
    special = "special"
    shield = "shield"
    resource = "resource"


class World(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    creator_id: Optional[int] = Field(default=None, foreign_key="player.id")
    creator: Optional["Player"] = Relationship(
        back_populates="personal_world", sa_relationship_kwargs={"foreign_keys": "[World.creator_id]"}
    )

    inhabitants: List["Player"] = Relationship(
        back_populates="current_world", sa_relationship_kwargs={"foreign_keys": "[Player.current_world_id]"}
    )


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    in_game_name: Optional[str]
    slack_id: str = Field(index=True)
    api_token: str = Field(index=True)
    token_last_updated: datetime.datetime

    pos_x: int = Field(default=0)
    pos_y: int = Field(default=0)

    inventory: List["Item"] = Relationship(back_populates="player")
    
    level: int = Field(default=1, le=100)
    xp: int = Field(default=0, lt=1000)
    
    personal_world: Optional["World"] = Relationship(
        back_populates="creator", sa_relationship_kwargs={"foreign_keys": "[World.creator_id]"}
    )

    current_world_id: Optional[int] = Field(default=None, foreign_key="world.id")
    current_world: Optional["World"] = Relationship(
        back_populates="inhabitants", sa_relationship_kwargs={"foreign_keys": "[Player.current_world_id]"}
    )


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: ItemCategory
    cost: Optional[Decimal] = None
    can_be_sold: bool = Field(default=False)
    is_breakable: bool = Field(default=False)
    hitpoints_remaining: Optional[Decimal] = None

    player_id: Optional[int] = Field(default=None, foreign_key="player.id")
    player: Optional[Player] = Relationship(back_populates="inventory")
