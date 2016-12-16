from utils import *

def test_celestial_dreamer():
	game = prepare_game()
	dreamer = game.player1.give("CFM_617")
	assert not dreamer.powered_up

	wisp = game.player1.give(WISP).play()
	po = game.player1.give("EX1_316").play(target=wisp) #Power Overwhelming

	assert dreamer.powered_up

	dreamer.play()
	assert dreamer.buffs
	assert dreamer.atk == 5
	assert dreamer. health == 5

def test_virmen_sensei():
	game = prepare_empty_game()
	sensei1 = game.player1.give("CFM_816")
	wisp = game.player1.give(WISP).play()
	assert not sensei1.powered_up

	sensei1.play()

	beast = game.player1.give(CHICKEN).play()
	sensei2 = game.player1.give("CFM_816")
	assert sensei2.powered_up
	game.player1.give(INNERVATE).play()
	sensei2.play(target=beast)

	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

def test_mark_of_the_lotus():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	chicken = game.player1.give(CHICKEN).play()

	assert wisp.atk == 1
	assert chicken.atk == 1
	lotus = game.player1.give("CFM_614").play()

	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert chicken.buffs
	assert chicken.atk == 2
	assert chicken.health == 2

def test_pilfered_power():
	game = prepare_game(game_class=Game)
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	assert game.player1.max_mana == 3
	pilfered1 = game.player1.give("CFM_616")
	pilfered1.play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 3
	assert game.player1.max_mana == 3

	game.end_turn(); game.end_turn()

	assert game.player1.max_mana == 4
	livingroots = game.player1.give("AT_037").play(choose="AT_037b")
	assert len(game.player1.field) == 2
	pilfered2 = game.player1.give("CFM_616").play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 4 + 2
	assert game.player1.max_mana ==  4 + 2

	for i in range(4):
		game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 10
	pilfered3 = game.player1.give("CFM_616").play()
	assert len(game.player1.hand) == 1
	assert game.player1.max_mana == 10
	excess_mana = game.player1.hand[0]
	assert excess_mana.id == "CS2_013t"
	excess_mana.play()
	assert len(game.player1.hand) == 1

def test_lunar_visions():
	game = prepare_empty_game()
	golem = game.player1.give("CS2_186").shuffle_into_deck() #War Golem
	portal = game.player1.give(UNSTABLE_PORTAL).shuffle_into_deck()

	game.player1.give("CFM_811").play()
	assert len(game.player1.hand) == 2
	def check_cost(c):
		if c.id == "CS2_186":
			assert c.cost == 5
		else:
			assert c.cost == 2
	for c in game.player1.hand:
		check_cost(c)

def test_alleycat():
	game = prepare_game()
	game.player1.give("CFM_315").play()
	assert len(game.player1.field) == 2
	assert game.player1.field[0].id == "CFM_315"
	assert game.player1.field[1].id == "CFM_315t"

# def test_rat_pack():
# 	game = prepare_empty_game()
# 	ratpack = game.player1.give("CFM_316").play()
# 	timberwolf = game.player1.give("DS1_175").play()

# 	assert ratpack.atk == 3

# 	game.player1.give(SOULFIRE).play(target=ratpack)
# 	assert len(game.player1.field) == 4

# def test_dispatch_kodo():
# 	game = prepare_empty_game()
# 	kodo = game.player1.give("CFM_335")
# 	timberwolf = game.player1.give("DS1_175").play()
# 	kodo.play(target = game.player2.hero)

# 	assert game.player2.hero.health == 30 - 3

def test_shaky_zipgunner():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	gunner = game.player1.give("CFM_336").play()
	game.player1.give("CS2_057").play(target=gunner) #Shadow Bolt
	assert wisp.atk == 3
	assert wisp.health == 3

	wisp.play()

	assert wisp.atk == 3
	assert wisp.health == 3

def test_trogg_beastrager():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	trogg1 = game.player1.give("CFM_338").play()
	assert wisp.atk == 1
	beast = game.player1.give(CHICKEN)
	trogg2 = game.player1.give("CFM_338").play()
	assert beast.buffs
	assert beast.atk == 2
	assert beast.health == 2

	beast.play()

	assert beast.buffs
	assert beast.atk == 2
	assert beast.health == 2

def test_hidden_cache():
	game = prepare_empty_game()
	cache = game.player1.give("CFM_026").play()
	assert game.player1.secrets
	game.end_turn()
	game.player2.give(WISP).play()
	assert game.player1.secrets

	game.end_turn()
	wisp = game.player1.give(WISP)
	game.end_turn()
	game.player2.give(WISP).play()
	assert not game.player1.secrets
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3

	game.end_turn()

	wisp.play()
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3

def test_smugglers_crate():
	# Game allows card to be played with no beast in hand
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	crate = game.player1.give("CFM_334")
	beast = game.player1.give(CHICKEN)
	crate.play()
	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

	beast.play()
	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

def test_piranha_launcher():
	game = prepare_empty_game()
	game.player1.give("CFM_337").play()
	game.end_turn()
	wisp = game.player2.give(WISP).play()
	game.end_turn()
	game.player1.hero.attack(target=wisp)

	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "CFM_337t"

def test_kabal_lackey():
	game = prepare_empty_game()
	counterspell = game.player1.give("EX1_287")
	assert counterspell.cost == 3
	vaporize = game.player1.give("EX1_594")
	assert vaporize.cost == 3
	missiles = game.player1.give("EX1_277")
	assert missiles.cost == 1
	game.player1.give("CFM_066").play()
	assert counterspell.cost == 0
	assert vaporize.cost == 0
	assert missiles.cost == 1

	missiles.play()
	assert counterspell.cost == 0
	assert vaporize.cost == 0

	counterspell.play()
	assert vaporize.cost == 3

	game.player1.give("CFM_066").play()
	assert vaporize.cost == 0

	game.end_turn()
	assert vaporize.cost == 3
	game.end_turn()
	assert vaporize.cost == 3

def test_manic_soulcaster():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	game.player1.give(HAND_OF_PROTECTION).play(target=wisp)
	game.player1.give("CS2_236").play(target=wisp) #Inner Fire
	assert wisp.divine_shield
	assert wisp.health == 2
	game.player1.give("CFM_660").play(target=wisp)
	assert len(game.player1.deck) == 1

	game.end_turn()
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert not game.player1.hand[0].divine_shield
	assert game.player1.hand[0].health == 1

def test_cryomancer():
	game = prepare_empty_game()
	cryomancer = game.player1.give("CFM_671")
	assert not cryomancer.powered_up

	game.player1.give("CS2_031").play(target=game.player2.hero)
	assert cryomancer.powered_up
	cryomancer.play()
	assert cryomancer.buffs
	assert cryomancer.atk == 7
	assert cryomancer.health == 7

def test_inkmaster_solia():
	game = prepare_empty_game()
	btg = game.player1.give("AT_035")# Beneath the Grounds
	soulfire = game.player1.give(SOULFIRE)
	assert btg.cost == 3
	assert soulfire.cost == 1
	game.player1.give("CFM_687").play()
	assert btg.cost == 0
	assert soulfire.cost == 0
	btg.play()
	assert soulfire.cost == 1
	game.end_turn()

	game.player2.give(WISP).shuffle_into_deck()
	game.player2.give(WISP).shuffle_into_deck()
	solia = game.player2.give("CFM_687")
	mc = game.player2.give(MIND_CONTROL)
	solia.play()
	assert mc.cost == 10
	game.end_turn()
	game.end_turn()
	game.player2.give("CFM_687").play()
	assert mc.cost == 0
	game.end_turn()
	game.end_turn()
	assert mc.cost == 10

def test_potion_of_polymorph():
	game = prepare_game()
	game.player1.give("CFM_620").play()
	game.player1.give(WISP).play()
	assert game.player1.secrets
	game.end_turn()

	game.player2.give(WISP).play()
	assert len(game.player2.field) == 1
	assert game.player2.field[0].id == "CS2_tk1"
	assert not game.player1.secrets

def test_greater_arcane_missiles():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007").play()
	game.player1.give("CS2_004").play(target=acolyte) #Power Word: Shield
	game.player1.discard_hand()
	game.end_turn()
	game.player2.give(KOBOLD_GEOMANCER).play()
	game.player2.give("CFM_623").play()
	
	if acolyte.dead:
		assert len(game.player1.hand) == 2
		assert game.player1.hero.health == 30 - 4
	elif acolyte.health == 1:
		assert len(game.player1.hand) == 1
		assert game.player1.hero.health == 30 - 8
	elif acolyte.health == 5:
		assert len(game.player1.hand) == 0
		assert game.player1.hero.health == 30 - 12
	else:
		assert False

def test_red_mana_wyrm():
	game = prepare_game()
	wyrm = game.player1.give("CFM_060").play()
	assert wyrm.atk == 2

	game.player1.give(INNERVATE).play()
	assert wyrm.atk == 4

	game.player1.give(CIRCLE_OF_HEALING).play()
	assert wyrm.atk == 6

def test_hozen_healer():
	game = prepare_empty_game()
	blademaster1 = game.player1.give("CS2_181").play()
	assert blademaster1.health == 3
	game.player1.give("CFM_067").play(target=blademaster1)
	assert blademaster1.health == 7
	game.end_turn()

	game.player2.give("EX1_591").play()
	game.player2.give("CFM_067").play(target=blademaster1)
	assert blademaster1.dead

def test_kabal_chemist():
	game = prepare_empty_game()
	game.player1.give("CFM_619").play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id in fireplace.cards.utils.POTIONS