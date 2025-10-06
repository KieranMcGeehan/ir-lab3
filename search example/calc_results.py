
import json
import os
import sys
import nltk
nltk.download('stopwords')


from inverted_index import InvertedIndex
from utils import read_data

out = sys.argv[1]
print(f"Outputting to {out}")

results = {}

for weighting_scheme in ["TF", "TF-IDF", "Log-Entropy"]:
    inv_ind = InvertedIndex()

    documents = read_data("./shakespeare")

    print(f"Weighing scheme {weighting_scheme}")
    pad = len(str(len(documents)))
    for (i, d) in enumerate(documents):
        inv_ind.add_document(d)
        print(f"Loading documents... {str(i).rjust(pad, " ")}/{len(documents)}")

    if weighting_scheme == "TF":
        inv_ind.generate_term_by_doc_matrix()
    elif weighting_scheme == "TF-IDF":
        inv_ind.calcTFIDF()
        inv_ind.generate_term_by_doc_matrix(tfidf = True)
    elif weighting_scheme == "Log-Entropy":
        inv_ind.calcLogEntropy()
        inv_ind.generate_term_by_doc_matrix(log_entropy = True)
    else:
        raise Exception(":'(")

    weighing_results = {}
    for comp_metric in ["cosine", "euclidian", "pearson", "spearman", "taxicab"]:
        print(f"Searching {weighting_scheme} using {comp_metric}")
        r = inv_ind.search("scotland kings and thanes", tfidf=(weighting_scheme=="TF-IDF"), log_entropy=(weighting_scheme=="Log-Entropy"), comparison=comp_metric)
        r = [[k,v] for (k,v) in r]
        weighing_results[comp_metric] = r
    results[weighting_scheme] = weighing_results

with open(out, "w") as f:
    f.write(json.dumps(results))