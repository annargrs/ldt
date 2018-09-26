===========================================
Combining information from ldt word objects
===========================================

All the information from various LDT resources is combined in the :class:`~ldt.relations.pair.RelationsInPair` class.
Similarly to the :class:`~ldt.relations.word.Word`, it can work on raw string input and initialize all the necessary
resources with default parameters. You can also pass pre-initialied dictionary objects (normalizer, derivation,
lexicographic and distributional dictionaries) for faster processing on scale. See the docstring of :class:`~ldt.relations.pair.RelationsInPair` for the full list of options.

The output of this function is a dictionary with binary or numerical values for this given word pair that correspond to `ld variables <http://ldtoolkit.space/ldscores/>`_. Only non-False values are returned, i.e. if a variable is not in the dictionary, the relation is missing.

The basic usage is as follows:

>>> relation_analyzer = ldt.relations.RelationsInPair()
>>> relation_analyzer.analyze("black", "white")
{'Hyponyms': True,
 'SharedMorphForm': True,
 'SharedPOS': True,
 'Synonyms': True,
 'Antonyms': True,
 'ShortestPath': 0.058823529411764705,
 'Associations': True,
 'TargetFrequency': 491760,
 'NeighborFrequency': 509267}
>>> relation_analyzer.analyze("kindness", "happiness")
{'Synonyms': True,
 'SharedDerivation': True,
 'SharedMorphForm': True,
 'SharedPOS': True,
 'ShortestPath': 0.08333333333333333,
 'Associations': True,
 'TargetFrequency': 5119,
 'NeighborFrequency': 14543}

``silent=False`` option exectutes :meth:`~ldt.relations.word.Word.pp_info` function for visual inspection of the information available for the input words.

>>> relation_analyzer.analyze("humanist", "anti-humanist", silent=False)
====== HUMANIST ======
====== MORPHOLOGICAL INFO ======
OriginalForm :  humanist
POS :  noun, adjective
IsLemma :  True
Lemmas :  humanist
====== DERIVATIONAL INFO ======
Stems :  humane, human, hum, hume
Suffixes :  -an, -ist
Prefixes :
OtherDerivation :
RelatedWords :  human genome project, humaneness, human life, humankind, human capital, human, human movement, human death, humanity, human chorionic gonadotropin, human nature, human development, human immunodeficiency virus, human kind, human papillomavirus, humanize, human chattel, hummer, humming, inhuman, humanization, humanness, human condition, human botfly, humanism, human resources, hum, humanly, to err is human, human-computer interaction, hummingbird, inhumane, nonhuman, human insulin, non-human, human pyramid, humming-top, human race, human interest, humanist, human rights, human trafficking, human knot, human being, humanoid, humanizer, humanely, human behaviour, human relations
====== SEMANTIC INFO ======
Synonyms :  human-centred, human-centered, humane, humanitarian, humanist, humanistic
Antonyms :  nonhumanist, inhumane
Meronyms :
Hyponyms :  litterateur, desiderius_erasmus_roterodamus, erasmus_von_rotterdam_erasmus, geert_geerts, chysoloras,_manuel, d._erasmus, paul_kurtz, desidarius_erasmus, erasmus_of_rotterdam, raumsol, rotterdamensis, erasmus_roterodamus, intellectal, chrysoloras, philologist, gerhard_gerhards, humanist_marxism, public_intellectual, erasmus_rotterdam, man_of_letters, erasmus,_desiderius, disiderius_erasmus_of_rotterdam, roterodamus, eramus, intelligentsia, p._w._kurtz, erasmus_von_rotterdam, marxist-humanism, thinkers, well_read, erasmian, classicist, philologue, litterateur_engage, levi_fragell, homme_de_lettres, erasmus, marxist_humanist, bernat_metge, public_intellectuals, marxist_humanism, intelectual, homme_des_lettres, intellectuals, tudós, clerisy, gerrit_gerritszoon, desiderius_erasmus_of_rotterdam, optima, carlos_bernardo_gonzález_pecotche, optima_nova, institute_for_science_and_human_values, erasmism, carlos_bernardo_gonzalez_pecotche, literatus, desiderus_erasmus, desiderius_erasmus, littérateur, eupraxsophy, edwin_h._wilson, marxist_humanists, paul_kurts, prince_of_the_humanists, well-read, intellectual, manuel_chysoloras, littérateur_engagé, chrysoloras,_manuel, classical_scholar, eupraxsophies, ff_din, manuel_chrysoloras, eupraxosophy, eupraxophy
Hypernyms :  topical_outline_of_humanism, legislative_ethics, condensed_font, ὑπόθεσις, bookshop, bookselling, teachings, variable-width_font, humanists, secularhumanism, metric-compatible, code_of_ethics, sample_of_font, senior_seminar, possibility, theoretic, religious_doctrines, typographic_measurement, booksellers, bookseller, shadow_typeface, ethic, theories, myth_theorist, secular_humanitarianism, scholars, topic_outline_of_humanism, ascent, bookstores, printer_font, scholarly_method, schools_of_thought, 🗚, non-character_typefaces, hypothetically, type-face, ism, fount, merely_a_theory, draft:humanism, religious_doctrine, liberal_humanism, secular_rationalism, case, proportional_figures, secularism,_secular_humanism, intellectual_tradition, font_width, shadowed_typeface, type_font, face, humanized, seminar, hypoth, college_bookstore, tabular_figures, ethics_code, scholarly_person, theorized, hypothesis, antiquarian_bookseller, expert_set, scientific_humanism, hypotheses, codes_of_ethics, scientific_humanist, inline_font, shadowed_font, exponent, humanism, engraved_font, font_style, theory_of, school_of_thought, display_type, theoretical_approach, seminars, theorists, theorist, radical_humanism, type_face, antecedent, proportional_spacing, doctrine, secular_humanist, educational_organisation, stylistic_sets, theory_and_practice, typeface, bookman, hypothesized, student, type_faces, book_shops, scientific_question, book_retail, philosophy, myth_theories, non-proportional_font, book_sellers, proponent, political_doctrine, descent, theoretical_model, engraved_typeface, just_a_theory, intellectual_traditions, humanize, secular_humanism_old, alternative_theories, book_selling, optical_size, guided_experience, list_of_humanism_topics, stroke_weight, variable_width_font, alternative_theory, scientific_hypothesis, hypothesize, educational_organization, a_theory_of, bookshoppe, schoolbook_characters, variable-width, type, humanist, scholar, expert_font, ethical_codes, proportional_fonts, humanistic, scholarly, book_sales, secular_humanists, humanist_philosopher, book_shop, philosophical_system, scholarship, theoretical, progressive_humanist, advocate, secular_humanism, book_store, scholarly_research, stylistic_alternate, type-faces, font_family, shadow_font, school, display_typeface, stylistic_set, typeface_family, sale_of_books, book_sale, inline_typeface, doctrinal, optical_sizes, theory, theory_and_fact, embed_font, font, clawrite, typefaces, list_of_scientific_theories_and_laws, bookstore, seminar_college, advocator, theory-based_model, centaur_roman, font_weight, stylistic_alternates, doctrines, proportional_and_tabular_figures, 🗛, list_of_theories, font_sample, ethical_code, fonts
====== EXTRA WORD CLASSES ======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  False
Missing :  False
None
====== ANTI-HUMANIST ======
====== MORPHOLOGICAL INFO ======
OriginalForm :  anti-humanist
POS :  noun, adjective
IsLemma :  False
Lemmas :  anti
====== DERIVATIONAL INFO ======
Stems :  ante, ant
Suffixes :  -i
Prefixes :
OtherDerivation :
RelatedWords :  sugar ant, white ant, ants in ones pants, antkind, anteater, antshrike, ant beetle, velvet ant, ante, ant-bed, antly, antbear, anthill, antlike, antbird, anting, ant cap, the ants pants, antlion
====== SEMANTIC INFO ======
Synonyms :  anti
Antonyms :  pro
Meronyms :
Hyponyms :
Hypernyms :  individual,_individuality, individuals, person, record_company, perſon, soul, individual, mortal, individuality_individual, personhood_theory, persons, somebody, someone, a_person, perſons
====== EXTRA WORD CLASSES ======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  True
Missing :  False
|
{'SharedPOS': True,
 'Synonyms': True,
 'ShortestPath': 0.2,
 'TargetFrequency': 6469,
 'NeighborFrequency': 0}