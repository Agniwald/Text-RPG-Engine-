from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


players_moves = Table('players_moves',
	Base.metadata,
	Column('player_id', Integer, ForeignKey('players.id')),
	Column('move_id', Integer, ForeignKey('moves.id'))
	)


class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    user = Column(String)
    strength = Column(Integer, default=5)
    agility = Column(Integer, default=5)
    intelligence = Column(Integer, default=5)
    charisma = Column(Integer, default=5)
    luck = Column(Integer, default=5)
    xp = Column(Integer, default=100)
    weapon_id = Column(Integer, ForeignKey('weapons.id'), default=1)
    armor_id = Column(Integer, ForeignKey('armors.id'), default=1)
    inventory_id = Column(Integer, ForeignKey("inventories.id"))
    moves = relationship("Move", secondary=players_moves, backref=backref('players', lazy='dynamic'))


class Weapon(Base):
	__tablename__ = 'weapons'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	damage = Column(Integer)
	players = relationship("Player", backref="weapon")


class Armor(Base):
	__tablename__ = 'armors'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	protection = Column(Integer)
	players = relationship("Player", backref="armor")


inv_subj = Table('inv_subj',
	Base.metadata,
	Column('inventory_id', Integer, ForeignKey('inventories.id')),
	Column('subject_id', Integer, ForeignKey('subjects.id'))
	)


class Inventory(Base):
	__tablename__ = 'inventories'
	
	id = Column(Integer, primary_key=True)
	coins = Column(Integer)
	player = relationship("Player", uselist=False, backref="inventory")
	subjects_in_inverntories = relationship("Subject", secondary=inv_subj, backref=backref('subjs_in_invs', lazy='dynamic'))


class Subject(Base):
	__tablename__ = 'subjects'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)


class Mob(Base):
    __tablename__ = 'mobs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    strength = Column(Integer)
    agility = Column(Integer)
    xp = Column(Integer)
    moves = relationship("Move", backref="mob")


class Move(Base):
	__tablename__ = 'moves'
    
	id = Column(Integer, primary_key=True)
	text = Column(Text)
	no_access_text = Column(Text)
	finished_text = Column(Text)
	access = relationship("Access", uselist=False, backref="move")
	fight = Column(Boolean, default=False)
	choices = relationship("Choice", backref="move")
	mob_id = Column(Integer, ForeignKey('mobs.id'))
	awards = relationship("Award", backref="move")
	next = Column(Integer)


class Choice(Base):
	__tablename__ = 'choices'
  
	id = Column(Integer, primary_key=True)
	text = Column(String)
	next = Column(Integer)
	finished = Column(Boolean)
	move_id = Column(Integer, ForeignKey('moves.id'))


class Award(Base):
	__tablename__ = 'awards'
    
	id = Column(Integer, primary_key=True)
	type = Column(String)
	quantity = Column(Integer)
	award_id = Column(Integer)
	move_id = Column(Integer, ForeignKey('moves.id'))


class Access(Base):
	__tablename__ = 'accesses'
    
	id = Column(Integer, primary_key=True)
	type = Column(String)
	quantity = Column(Integer)
	stay = Column(Boolean)
	move_id = Column(Integer, ForeignKey("moves.id"))
