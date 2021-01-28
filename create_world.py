from models import *
import json


# drop and create all tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# create inventory
i = Inventory(coins=5)
session.add(i)
session.commit()


# create player
p = Player(inventory=i)
session.add(p)
session.commit()


# create mobs
with open('world/mobs.json') as f:
	mobs = json.load(f)['mobs']

for mob in mobs:
	m = Mob(name=mob["name"], strength=mob["strength"], agility=mob["agility"], xp=mob["xp"])
	session.add(m)
	session.commit()


# create subjects
with open('world/subjects.json') as f:
	subjects = json.load(f)['subjects']

for sub in subjects:
	s = Subject(name=sub)
	session.add(s)
	session.commit()


# create weapons
with open('world/weapons.json') as f:
	weapons = json.load(f)['weapons']

for weap in weapons:
	w = Weapon(name=weap["name"], damage=weap["damage"])
	session.add(w)
	session.commit()


# create armors
with open('world/armors.json') as f:
	armors = json.load(f)['armors']

for ar in armors:
	a = Armor(name=ar["name"], protection=ar["protection"])
	session.add(a)
	session.commit()

# create moves
with open('world/moves.json') as f:
	moves = json.load(f)['moves']

for move in moves:
	# add access
	if move["access"]:
		access = move["access"]
		acc = Access(type=access["type"], quantity=access["quantity"], stay=access["stay"])
		session.add(acc)
		session.commit()
	else:
		acc = None

	if move["mob"]:
		mob = session.query(Mob).filter_by(name=move["mob"]).first()
	else:
		mob = None

	m = Move(text=move["text"], no_access_text=move["no_access_text"],
		finished_text=move["finished_text"], fight=move["fight"],
		next=move["next"], mob=mob, access=acc)
	session.add(m)
	session.commit()

	# add choices
	choices = move["choices"]
	for ch in choices:
		c = Choice(text=ch["text"], next=ch["next"], finished=ch["finished"], move=m)
		session.add(c)
		session.commit()

	# add awards
	if "awards" in move.keys():
		awards = move["awards"]
		for aw in awards:
			a = Award(type=aw["type"], quantity=aw["quantity"], move=m, award_id=aw["award_id"])
			session.add(a)
			session.commit()
