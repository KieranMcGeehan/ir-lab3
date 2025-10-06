
import nltk
nltk.download('stopwords')


from inverted_index import InvertedIndex
from utils import read_data
inv_ind = InvertedIndex()

documents = read_data("./data")
documents += read_data("./shakespeare")

for d in documents:
    inv_ind.add_document(d)