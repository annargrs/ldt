# Linguistic Diagnostics Toolkit

The only way of exploring linguistic relations in a distributional space that
is currently used are various techniques for evaluating distances between word
(sentence, morpheme) vectors. The intuition is that words that are more
similar, and therefore occur in similar contexts, should also be closer in the
space than unrelated words: e.g. *cat* should be closer to *dog* than to
*banana*. However, there are two problems with such distributional similarity:

 * Unless the model has been previously specialized, the distributional
   similarity conflates a wide range of linguistic relations: e.g. *cats*,
   *kitten*, *milk* and *chase* could all be expected to be closer to *cat*
   than to *dog*.
 * While both humans and word embeddings are generally good at distinguishing
   related from unrelated words, ranking the middle ground is more problematic.
   For example, should *cat* be closer to *tiger* or to *purr*?

 LDT is based on the idea that all the different relations in distributional
 similarity are all useful in different contexts (i.e. extrinsic tasks), and
 the different algorithms that produce them should be studied from the point of
 view of their favoring certain types of relations over the others. The only
 way to do this is to look into the output of the model and find out what
 exactly it is doing.

 To this end, LDT provides a set of tools for automatic annotation of a wide
 range of distributional and linguistic relations between words and their
 neighbors in the distributional space. It currently handles the following
 types of relations between a target word and its neighbor:

 * misspellings (*cat : kat*);
 * inflected forms (*cat : cats*);
 * derivational relations (*cat : catness*);
 * lexicographic semantic relations:
   - synonymy (*cat : pussycat*);
   - antonymy (*black : white*);
   - hyperonymy (*cat : feline*);
   - hyponymy (*feline : cat*);
   - co-hyponymy (*cat : dog*);
   - meronymy (*cat : tail*)
 * psychological association norms (cat : mouse)
 * corpus-based statistics (e.g. for *cat : mouse* pair the frequency of
   *mouse* in the corpus in general and in the context of *cat* in particular);
 * broad world knowledge (*cat : breed*, *cat : owner*, *cat : milk*)

LDT achieves the above by combining several resources, including dictionaries
(WordNet, Wiktionary, BabelNet), psychological association norms resources
(Edinburgh Associative Thesaurus, University of South Florida Free
Association Norms), data from several corpora, including Wikipidea and Gogle
Ngrams, and custom routines for advanced morphological analysis,
lemmatization, compound splitting, and identification of productive affixes.

In addition to being useful in research and for exploratory purposes, LDT can
be viewed as a method of intrinsic evaluation of word emeddings. While there
is a range of intrinsic tasks that such models are traditionally evaluated
on (correlation with human similarity judgements or word analogy task),
these approaches have failed to be good predictors of how a given model
would perform on particular task. Furthermore, they offer little insight
about what kind of linguistic information such models actually capture. Since
LDT provides that information, it could be used to estimate to what extent a
given model should be useful for a task that relies e.g. on morphological
knowledge.
