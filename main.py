from models import *
from helpers import *
import create_world


player = session.query(Player).first()


def make_move(player, move_id, prev_id):
	# get current move
	move = session.query(Move).filter_by(id=move_id).first()

	# check move status
	if not check_move_status(player, move):

		# check access
		if check_access(player, move):
			print("\n" + move.text)

			# if awards and not fight -> give award
			if move.awards and not move.fight:
				give_awards(player, move.awards)

			# if fight
			if move.fight:
				win = fight(player, move.mob)
				
				# give awards if win
				if win:
					# change status of current move to finished
					player.moves.append(move)
					give_awards(player, move.awards)

				# go to the next move
				make_move(player, move.next, move_id)

			# make decision
			id_of_next_move = make_decision(player, move, False)

			# change status of current move to finished
			player.moves.append(move)

			# make next move
			make_move(player, id_of_next_move, move_id)

		else:
			# if access not granted -> print accessable text and return to prev move 
			print("\n" + move.no_access_text)
			move = session.query(Move).filter_by(id=prev_id).first()
			make_move(player, prev_id, prev_id)

	else:
		print("\n" + move.finished_text if move.finished_text else "\n" + move.text)
		id_of_next_move = make_decision(player, move, True)
		move = session.query(Move).filter_by(id=id_of_next_move).first()
		make_move(player, id_of_next_move, move_id)


make_move(player, 1, 1)
