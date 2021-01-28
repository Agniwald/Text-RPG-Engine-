from models import *
import random
import time


def player_profile(player):
	print("\n\tПрофиль игрока")
	print("Сила:", player.strength)
	print("Ловкость:", player.agility)
	print("Интеллект:", player.intelligence)
	print("Харизма:", player.charisma)
	print("Удача:", player.luck)
	print("Здоровье:", player.xp)
	print("Оружие:", player.weapon.name, player.weapon.damage, "урона")
	print("Броня:", player.armor.name, player.armor.protection, "защиты")
	print(f"Инвентарь: {player.inventory.coins} монет")
	for i in player.inventory.subjects_in_inverntories:
		print("\t", i.name)
	print()


def check_move_status(player, move):
	return True if move in player.moves else False


def make_decision(player, move, finished):
	next_moves_map = {}
	count = 1
	for i in range(len(move.choices)):
		if move.choices[i].finished == finished:
			print(f"{count}. {move.choices[i].text}")
			next_moves_map[count] = move.choices[i].next
			count += 1

	# if there is no "finished" choices
	if count == 1:
		for i in range(len(move.choices)):
			print(f"{count}. {move.choices[i].text}")
			next_moves_map[count] = move.choices[i].next
			count += 1

	if_exit = False
	next_move = count
	while next_move >= count or next_move < 0:
		try:
			next_move = int(input("Ваше действие? (1, 2, 3...) (0 для вывода профиля игрока; -1 для выхода) >> " ))
			if next_move == 0:
				player_profile(player)
			elif next_move == -1:
				if_exit = True
				break
		except:
			pass
	if if_exit:
		exit()
	return next_moves_map[next_move] if next_move > 0 else make_decision(player, move, finished)


def player_attack(player, mob):
	time.sleep(3)

	attack = random.randint(1, 20) + player.strength + player.weapon.damage
	mob_dodge = random.random() * 100 <= mob.agility

	if mob_dodge:
		print(f"{mob.name} уворачивается!")
	else:
		mob.xp -= attack
		print(f"Вы нанесли {attack} урона! У {mob.name} осталось {mob.xp} здоровья!")

	return True if mob.xp <= 0 else False


def mob_attack(player, mob):
	time.sleep(3)

	attack = random.randint(1, 20) + mob.strength - player.armor.protection
	player_dodge = random.random() * 100 <= player.agility
	
	if player_dodge:
		print("Вы смогли увернуться!")
	else:
		if attack > 0:
			player.xp -= attack
			print(f"{mob.name} нанес {attack} урона! У вас осталось {player.xp} здоровья!")
		else:
			print(f"Ваша защита полностью блокировала удар! У вас осталось {player.xp} здоровья!")

	return True if player.xp <= 0 else False


def fight(player, mob):
	player_profile(player)
	print(f"\n\tХарактеристики {mob.name}")
	print("Сила:", mob.strength)
	print("Ловкость:", mob.agility)
	print("Здоровье:", mob.xp)

	print("\n1. Сбежать")
	print("2. Начать бой")
	
	while True:
		next_move = input("Ваше действие? (1, 2) >> " )
		if next_move == "1":
			return False
		elif next_move == "2":
			break

	print("\nНАЧИНАЕТСЯ БОЙ\n")

	who_first = random.random()
	player_xp = player.xp
	mob_xp = mob.xp

	while True:
		if who_first > 0.5:
			if player_attack(player, mob):
				print(f"\nВы победили {mob.name}!")
				break
			if mob_attack(player, mob):
				print("!!!YOU DIED!!!")
				exit()
		else:
			if mob_attack(player, mob):
				print("!!!YOU DIED!!!")
				exit()
			if player_attack(player, mob):
				print(f"\nВы победили {mob.name}!")
				break

	# restore xp
	player.xp = player_xp
	mob.xp = mob_xp

	return True



def give_awards(player, awards):
	for award in awards:
		# WIN
		if award.type == "win":
			print("Вы победили короля демонов! Вся слава и деньги ваши!")
			exit()

		# COINS
		if award.type == "coins":
			player.inventory.coins += award.quantity
			print(f"+{award.quantity} монет! Теперь у тебя {player.inventory.coins} монет!")

		# STATS

		elif award.type == "strength":
			player.strength += award.quantity
			print(f"Ты получил +{award.quantity} к силе! Теперь у тебя {player.strength} очков силы!")

		elif award.type == "agility":
			player.agility += award.quantity
			print(f"Ты получил +{award.quantity} к ловкости! Теперь у тебя {player.agility} очков ловкости!")

		elif award.type == "intelligence":
			player.intelligence += award.quantity
			print(f"Ты получил +{award.quantity} к интеллекту! Теперь у тебя {player.intelligence} очков интеллекта!")

		if award.type == "charisma":
			player.charisma += award.quantity
			print(f"Ты получил +{award.quantity} к харизме! Теперь у тебя {player.charisma} очков харизмы!")

		elif award.type == "luck":
			player.luck += award.quantity
			print(f"Ты получил +{award.quantity} к удаче! Теперь у тебя {player.luck} очков удачи!")

		# XP
		elif award.type == "xp":
			player.xp += award.quantity
			print(f"Ты получил +{award.quantity} к здоровье! Теперь у тебя {player.xp} очков здоровья!")

		# WEAPON
		elif award.type == "weapon":
			new_weapon = session.query(Weapon).filter_by(id=award.award_id).first()

			print(f"Ты можешь поменять свой {player.weapon.name} с {player.weapon.damage} очками урона на {new_weapon.name} с {new_weapon.damage} очками урона!")
			while True:
				answer = input("Принимаешь? (д/н) >> ")
				if answer == "д":
					player.weapon = new_weapon
					print("Отлично! Новое оружие!")
					break
				elif answer == "н":
					print("Это твой выбор.")
					break

		# ARMOR
		elif award.type == "armor":
			new_armor = session.query(Armor).filter_by(id=award.award_id).first()

			print(f"Ты можешь поменять свой {player.armor.name} с {player.armor.protection} очками защиты на {new_armor.name} с {new_armor.protection} очками защиты!")
			while  True:
				answer = input("Принимаешь? (д/н) >> ")
				if answer == "д":
					player.armor = new_armor
					print("Отлично! Новая броня!")
					break
				elif answer == "н":
					print("Это твой выбор.")
					break

		# OTHER SUBJECTS
		elif award.type == "subject":
			s = session.query(Subject).filter_by(id=award.award_id).first()
			player.inventory.subjects_in_inverntories.append(s)
			print(f"Теперь у тебя есть {s.name} в твоем инвентаре!")

	session.commit()
	# player_profile(player)


def check_access(player, move):
	
	if move.access is None:
		return True

	# COINS
	if move.access.type == "coins":
		if player.inventory.coins >= move.access.quantity:
			player.inventory.coins -= move.access.quantity
			return True
		else:
			return False

	# STATS

	elif move.access.type == "strength":
		return True if player.strength >= move.access.quantity else False

	elif move.access.type == "agility":
		return True if player.agility >= move.access.quantity else False

	elif move.access.type == "intelligence":
		return True if player.intelligence >= move.access.quantity else False

	elif move.access.type == "charisma":
		return True if player.charisma >= move.access.quantity else False

	elif move.access.type == "luck":
		return True if player.luck >= move.access.quantity else False

	# XP 
	elif move.access.type == "xp":
		return True if player.xp >= move.access.quantity else False

	# WEAPON 
	elif move.access.type == "weapon":
		return True if player.weapon.id == move.access.quantity else False

	# ARMOR 
	elif move.access.type == "armor":
		return True if player.armor.id == move.access.quantity else False

	# OTHER SUBJECTS 
	elif move.access.type == "subject":
		s = session.query(Subject).filter_by(id=move.access.quantity).first()
		return True if s in player.inventory.subjects_in_inverntories else False
