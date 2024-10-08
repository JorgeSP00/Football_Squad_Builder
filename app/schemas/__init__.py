from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    nationality_id = Column(Integer, ForeignKey('nationality.id'), nullable=True)
    market_value = Column(Float, nullable=True)
    position = Column(String, nullable=True)
    alternate_position = Column(String, nullable=True)


class Formation(Base):
    __tablename__ = 'formation'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Limitation(Base):
    __tablename__ = 'limitation'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    squad_id = Column(Integer, ForeignKey('squad.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competition.id'), nullable=False)
    budget = Column(Float, nullable=True)
    nationality_id = Column(Integer, ForeignKey('nationality.id'), nullable=True)


class Nationality(Base):
    __tablename__ = 'nationality'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    squad_id = Column(Integer, ForeignKey('squad.id'), nullable=False)
    value = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)


class Squad(Base):
    __tablename__ = 'squad'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    formation_id = Column(Integer, ForeignKey('formation.id'), nullable=False)


class SquadPlayer(Base):
    __tablename__ = 'squad_player'
    id = Column(Integer, primary_key=True, index=True)
    squad_id = Column(Integer, ForeignKey('squad.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    position_in_squad = Column(String, nullable=False)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class TeamCompetition(Base):
    __tablename__ = 'team_competition'
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competition.id'), nullable=False)