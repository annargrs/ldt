"""
Simple demo of using LDT for analysis of word embeddings with a small
vocabulary sample.

"""

import os
import vecto.embeddings
import pandas as pd

import ldt
from ldt.load_config import config as config
from ldt.relations.pair import RelationsInPair as RelationsInPair

def ldt_demo(top_n):

    # loading sample data
    sample_path = os.path.join(config["path_to_resources"], "sample_embeddings")
    out_path = os.path.join(sample_path, "demo_results.tsv")
    sample_vocab = ["cat", "dog", "walk", "buy", "pretty", "new", "often",
                    "rare"]
    embeddings = vecto.embeddings.load_from_dir(sample_path)
    embeddings.normalize()
    top_n = 10 #number of neighours to retrieve

    # setting up LDT resources
    normalizer = ldt.dicts.normalize.Normalization(language="English",order=(
        "wordnet", "custom"), lowercasing=True)
    DerivationAnalyzer = ldt.dicts.derivation.meta.DerivationAnalyzer()
    LexDict = ldt.dicts.metadictionary.MetaDictionary()

    analyzer = ldt.relations.pair.RelationsInPair(normalizer=normalizer,
                                                   derivation_dict =
                                                   DerivationAnalyzer,
                                                   lex_dict=LexDict)

    # retrieving neighbors
    neighbors = {}
    for word in sample_vocab:
        neighbors[word] = []
        neighbor_list = embeddings.get_most_similar_words(word,cnt=top_n+1)[1:]
        for neighbor in neighbor_list:
            neighbors[word].append(neighbor[0])

    # doing the analysis
    relations_of_interest = ["Synonyms", "Antonyms", "SharedPOS",
                             "SharedMorphForm", "SharedDerivation"]
    results = {x:0 for x in relations_of_interest}

    for target in neighbors:
        for neighbor in neighbors:
            relations = analyzer.analyze(target, neighbor)
            for rel in relations_of_interest:
                if rel in relations:
                    results[rel] += 1

    for relation in results:
        results[relation] = round(results[relation]/top_n, 2)

    df = pd.DataFrame.from_dict(results, orient="index")
    df.columns = ["LD scores"]

    df.to_csv(out_path, sep="\t", index=False, header=True)
    print(df)

if __name__ == "__main__":
    ldt_demo(10)





