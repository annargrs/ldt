=====================================================
Collecting all available information for a given word
=====================================================

LDT's :meth:`~ldt.relations.word.Word` class provides a convenient way to
configure several resources and combine them for repeated queries. This
class outputs a dictionary that records various properties of the queried word.

The first step of this analysis is input normalization described in section
:ref:`Normalization and classification of input strings`.

Once a word entry has been detected in one of configured lexicographic
resources, LDT collects the words that are related to the queried word with
various lexicographic relations. Derivational analysis is also performed to
detect both derived words and word stems/affixes.

Word class takes the following parameters:

    :original_spelling: the word to lookup (str)
    :normalizer: ldt.dicts.Normalizer() instance
    :derivation_dict:     ldt.dicts.derivation.DerivationAnalyzer() instance
    :metadictionary:  ldt.dicts.semantics.MetaDictionary() instance

You can leave it to LDT to initialize the default dictionary parameters, or
    you can pass your own objects, having set them up to your liking. This
        also saves time on initializing dictionaries in large-scale experiments.

All information is collected automatically from all the above resources upon
initialization of a Word object. The information can later be accessed
as a Python dictionary in the ``info`` attribute of that object:

>>> cat = ldt.Word("cat")
>>> cat.info
{'Antonyms': frozenset({'keep_down', 'rehabilitate'}),
 'Filenames': False,
 'ForeignWords': False,
 'Hashtags': False,
 'Hypernyms': frozenset({'adult_female', 'adult_male', 'animal', 'carnivore', 'creature', 'egest', 'eliminate', 'excitant', 'excrete', 'felid', 'feline', 'flog', 'gossip', 'gossiper', 'gossipmonger', 'lash', 'lather', 'mammal', 'man', 'newsmonger', 'pass', 'rumormonger', 'rumourmonger', 'slash', 'stimulant', 'stimulant_drug', 'strap', 'tracked_vehicle', 'trounce', 'vertebrate', 'welt', 'whip', 'woman', 'x-radiation', 'x-raying'}'}),
 'Hyponyms': frozenset({'acinonyx_jubatus', 'cheetah', 'chetah', 'domestic_cat', 'felis_catus', 'felis_domesticus', 'felis_onca', 'house_cat', 'housecat', 'jaguar', 'king_of_beasts', 'kitten', 'leopard', 'liger', 'lion', 'malkin', 'mouser', 'ounce', 'panther', 'panthera_leo', 'panthera_onca', 'panthera_pardus', 'panthera_tigris', 'panthera_uncia', 'saber-toothed_tiger', 'sabertooth', 'snow_leopard', 'sod', 'tiger', 'tiglon', 'tigon', 'tomcat', 'wildcat'}),
 'IsLemma': True,
 'Lemmas': frozenset({'cat'}),
 'Misspellings': False,
 'Noise': False,
 'Numbers': False,
 'OriginalForm': 'cat',
 'OtherDerivation': frozenset(),
 'POS': frozenset({'noun', 'verb'}),
 'Prefixes': frozenset(),
 'ProperNouns': False,
 'RelatedWords': frozenset(),
 'Stems': frozenset(),
 'Suffixes': frozenset(),
 'Synonyms': frozenset({'a feline', 'a pantherine', 'african_tea', 'arabian_tea', 'barf', 'be_sick', 'big_cat', 'bozo', 'cast', 'cat', "cat-o'-nine-tails", 'caterpillar', 'chuck', 'computed_axial_tomography', 'computed_tomography', 'computerized_axial_tomography', 'computerized_tomography', 'ct', 'disgorge', 'feliform', 'feline cat', 'feloid', 'grimalkin', 'guy', 'hombre', 'honk', 'housecat', 'kat', 'khat', 'kitten', 'kitty', 'machairodontini', 'malkin', 'metailurini', 'mog', 'moggy', 'mouser', 'panther', 'pantherine cat', 'puke', 'purge', 'puss', 'pussy', 'pussy-cat', 'qat', 'quat', 'queen', 'regorge', 'regurgitate', 'retch', 'saber-toothed cat', 'sick', 'smilodontini', 'spew', 'spue', 'tabby', 'throw_up', 'tom', 'tomcat', 'true_cat', 'upchuck', 'vomit', 'vomit_up'}),
 'URLs': False}

Since the primary use case of LDT is finding relations in pairs of words,
the lists of related words are currently stored as frozensets for efficiency.

You can pretty-print and group this information by categories with
:meth:`~ldt.relations.word.Word.pp_info()` method:

>>> encapsulation = ldt.Word("encapsulation")
>>> encapsulation.pp_info()
======DERIVATIONAL INFO======
Stems :  capsulate, encapsulate, capsule
Suffixes :  -ion, -ate
Prefixes :  en-
OtherDerivation :
RelatedWords :  encapsulation, capsule review, glissonian capsule, capsular, capsulate
======SEMANTIC INFO======
Synonyms :  encapsulation
Antonyms :
Meronyms :
Hyponyms :
Hypernyms :  physical_process, status, condition, process
======EXTRA WORD CLASSES======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  False
Missing :  False

If there are several lemmas, all the info will be pulled and combined for each of them:

>>> working = ldt.Word("working")
>>> working.pp_info()
======MORPHOLOGICAL INFO======
OriginalForm :  working
POS :  adjective, verb, noun
IsLemma :  False
Lemmas :  working, work
======DERIVATIONAL INFO======
Stems :
Suffixes :
Prefixes :
OtherDerivation :
RelatedWords :
======SEMANTIC INFO======
Synonyms :  form, workplace, effort, play, turn, work, draft, put_to_work, exercise, make, cultivate, functioning up, {{ws endlist}}, wreak, temporary, bring, act, running, forge, working, work_on, piece_of_work, basic, in employment, employment, figure_out, ferment, act_upon, oeuvre, go, also thesauruswork, influence, employed, process, operative, function, workings, run, sour, exploit, knead, make_for, mold, mould, puzzle_out, provisional, study, shape, on_the_job, body_of_work, solve, work_out, crop, do_work, operate, functional, also thesaurusoccupation, lick
Antonyms :  hobby, idle, take_away, malfunction, no-go, nonfunctional, sweeten, organic, sweet, inoperative, passing, broken, broken-down, {{ws endlist}}, standing, refrain, break, unemployment, come, down
Meronyms :  locker_room
Hyponyms :  assist, moonlight, coldwork, cut_out, publication, investigation, lumberyard, services, ironwork, travail, blackleg, work, oyster_bank, shipyard, coaching_job, handicraft, handwork, carpenter, spadework, jostle, follow-up, task, busywork, subbing, scab, attention, work_in_progress, putter, prey, public_service, cybernate, piscary, silverwork, rack, overcrop, telecommuting, specialize, keep_one's_shoulder_to_the_wheel, imprint, aid, turn_a_trick, coursework, tending, writing, telephone_exchange, peg_away, monkey, teleworking, polishing, reshape, bushwhack, mess_around, nightwork, preform, whore, slog, handbuild, work_at, caning, research_laboratory, piecework, lacework, remold, serve, knuckle_down, farm, collaborate, break_one's_back, science_lab, pull_wires, central, studio, overcultivate, washing, sculpt, fink, mound, stir, make-work, fish_farm, handiwork, resolve, freelance, paperwork, booking, fag, exercise, carry, monkey_around, drill_site, oyster_park, shining, swing, wicker, glassworks, paper_route, masticate, workload, overwork, rework, run_through, potter, answer, tannery, blackmail, labor, pressure, shop_floor, swage, slave, lavation, busy, loose_end, chip, oyster_bed, substituting, woodwork, hill, leatherwork, labour, get_together, heavy_lifting, mold, missionary_work, lacquerware, lab, cut, fill, intern, double, shop, muck_around, fishery, machine, known-working, buckle_down, plug_away, color, housework, seafaring, coil, model, specialise, tool, moil, make_hay, skimp, ministry, work_load, service, exchange, wash, toil, operation, ironing, welfare_work, cast, work_through, page, laundry, smithy, hot-work, swing_over, make_over, waterworks, {{ws endlist}}, hand-build, roughcast, logging, rope_yard, workpiece, minister, skipper, drudgery, blackjack, unfinished_business, bank, work_on, vinify, navigation, research_lab, prejudice, location, cold_work, scant, gasworks, join_forces, workshop, militate, project, followup, guess, keep_one's_nose_to_the_grindstone, retread, stamp, run, laboratory, action, procedure, exploit, wait, muck_about, sculpture, mould, care, upset, drudge, drive, infer, cooperate, job, warm_up, openwork, till, work_out, roll, ropewalk, brokerage, occupy, break, wickerwork, sinter, tinker, use, computerize, avail, form, social_service, bakeshop, man, play, creamery, colliery, beat, rat, masterpiece, dominate, pull_strings, metalwork, housewifery, test_bed, volunteer, handcraft, subcontract, manipulate, duty, roundhouse, clerk, claw, forge, boondoggle, puddle, sailing, help, feed, waitress, proving_ground, carve, engagement, get_at, pit, pull_one's_weight, mission, persuade, undertaking, strike, dig, polychrome, fix, prepossess, timework, layer, proof, sway, colour, bakehouse, beehive, brokerage_house, electioneer, riddle, bakery, chef-d'oeuvre, science_laboratory, housekeeping, investigating, throw, grind, beaver_away, take, go_through, coaching, computerise, beaver, ironworks
Hypernyms :  convert, turn, work, displace, production, touch_on, create_from_raw_stuff, utilize, business, apply, succeed, fascinate, capture, enchant, pass, understand, free_energy, geographic_point, stir, get, set, line, bear_upon, put_to_work, make, change_state, energy, excavation, trance, employ, bewitch, beguile, impact, transubstantiate, deal, activity, geographical_point, deliver_the_goods, gear_up, entrance, come_through, proceed, enamour, touch, ready, create_from_raw_material, {{ws endlist}}, acquisition, charm, affect, become, run, transform, care, go_across, job, line_of_work, stimulate, use, handle, transmute, move, manipulate, utilise, set_up, learning, create, becharm, prepare, occupation, go, enamor, bear_on, fix, manage, excite, output, catch, bring_home_the_bacon, captivate, end_product, go_through, win, operate, be, product
======EXTRA WORD CLASSES======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  False
Missing :  False

The same goes for tokenization error where two independent words were joined
together:

>>> tokenization_error = ldt.Word("livehappily")
>>> tokenization_error.pp_info()
======MORPHOLOGICAL INFO======
OriginalForm :  livehappily
POS :  adjective, adverb, verb
IsLemma :  False
Lemmas :  happily, live
======DERIVATIONAL INFO======
Stems :
Suffixes :
Prefixes :
OtherDerivation :
RelatedWords :
======SEMANTIC INFO======
Synonyms :  exist, bouncy, hold_out, lively, in the flesh, know, merrily, blithely, happily, resilient, gayly, jubilantly, living, go, go on, dwell see also thesaurusreside, survive, populate, in person, last, mirthfully, hot, experience, inhabit, remain see also thesauruspersist, live, subsist, alive, endure, dwell, live_on, springy, unrecorded, be, hold_up
Antonyms :  first, succumb, no-go, recorded, sadly, ignore, animated, broadcast, dull, cold, inexperience, neutral, prerecorded, dead, dummy, unhappily, blank, come
Meronyms :
Hyponyms :  bachelor, camp_out, tenant, reside, overpopulate, unlive, live_over, vegetate, wanton, cash_out, shack_up, swing, move, pig_it, domiciliate, perennate, bivouac, domicile, relive, lodge_in, pig, stand_up, freewheel, encamp, live_together, live_out, hold_water, neighbour, board, bach, room, cohabit, occupy, camp, neighbor, bushwhack, lodge, buccaneer, tent, nest, drift, taste, live_down, shack, dissipate, eke_out, hold_up, breathe, people
Hypernyms :  go_through, see, be, experience
======EXTRA WORD CLASSES======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  True
Missing :  False