from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, TIMESTAMP, Text, CheckConstraint
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    squads = relationship("Squad", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

class Nationality(Base):
    __tablename__ = 'nationality'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    players = relationship("Player", back_populates="nationality")

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)

    team_competitions = relationship("TeamCompetition", back_populates="competition")

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    players = relationship("Player", back_populates="team")
    team_competitions = relationship("TeamCompetition", back_populates="team")

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    nationality_id = Column(Integer, ForeignKey('nationality.id'))
    team_id = Column(Integer, ForeignKey('team.id'))
    market_value = Column(DECIMAL(15, 2), nullable=False)
    position = Column(String(50), nullable=False)
    alternate_position = Column(String(50))

    nationality = relationship("Nationality", back_populates="players")
    team = relationship("Team", back_populates="players")
    squad_players = relationship("SquadPlayer", back_populates="player")

class TeamCompetition(Base):
    __tablename__ = 'team_competition'
    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.id'), primary_key=True)

    team = relationship("Team", back_populates="team_competitions")
    competition = relationship("Competition", back_populates="team_competitions")

class Formation(Base):
    __tablename__ = 'formation'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    squads = relationship("Squad", back_populates="formation")

class Squad(Base):
    __tablename__ = 'squad'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('usuario.id'))
    formation_id = Column(Integer, ForeignKey('formation.id'))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    name = Column(String(50), nullable=False)
    competition_id = Column(Integer, ForeignKey('competition.id'))
    budget = Column(DECIMAL(15, 2))
    nationality_id = Column(Integer, ForeignKey('nationality.id'))

    user = relationship("Usuario", back_populates="squads")
    formation = relationship("Formation", back_populates="squads")
    squad_players = relationship("SquadPlayer", back_populates="squad")
    competition = relationship("Competition")
    nationality = relationship("Nationality")

class SquadPlayer(Base):
    __tablename__ = 'squad_player'
    id = Column(Integer, primary_key=True, index=True)
    squad_id = Column(Integer, ForeignKey('squad.id'))
    player_id = Column(Integer, ForeignKey('player.id'))
    position = Column(String(50), nullable=False)

    squad = relationship("Squad", back_populates="squad_players")
    player = relationship("Player", back_populates="squad_players")

class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('usuario.id'))
    squad_id = Column(Integer, ForeignKey('squad.id'))
    rating = Column(Integer, CheckConstraint('rating BETWEEN 0 AND 5'), nullable=False)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("Usuario", back_populates="ratings")
    squad = relationship("Squad")

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

class NationalityCreate(BaseModel):
    name: str

class CompetitionCreate(BaseModel):
    name: str
    region: str

class TeamCreate(BaseModel):
    name: str


# Posible positions.
class PositionEnum(str, Enum):
    GK = "GK"
    LB = "LB"
    CB = "CB"
    RB = "RB"
    CAM = "CAM"
    CM = "CM"
    CDM = "CDM"
    RM = "RM"
    LM = "LM"
    ST = "ST"
    RW = "RW"
    LW = "LW"

class PlayerCreate(BaseModel):
    name: str
    position: PositionEnum
    alternate_position: Optional[PositionEnum]
    team_id: int
    nationality_id: int
    market_value: Optional[float]

class SquadCreate(BaseModel):
    name: str
    formation_id: int
    user_id: int
    competition_id: Optional[int]
    nationality_id: Optional[int]
    budget: Optional[float]

class SquadPlayerCreate(BaseModel):
    squad_id: int
    player_id: int
    position: str

class TeamCreate(BaseModel):
    name: str

class TeamCompetitionCreate(BaseModel):
    team_id: int
    competition_id: int


class CompetitionCreate(BaseModel):
    name: str
    region: str

class FormationCreate(BaseModel):
    name: str
    description: Optional[str]

class NationalityCreate(BaseModel):
    name: str

class RatingCreate(BaseModel):
    user_id: int
    squad_id: int
    rating: float
    comment: Optional[str]

class UserCredentials(BaseModel):
    username: str
    password: str


