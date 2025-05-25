import argparse
from typing import Union
import numpy as np

from index_builer.inverted_index import InvertedIndex
from utils.utils import preprocess
from utils.encoding import decode_delta_single, decode_gamma_single


def search(input: str, query: str, encoding: Union[str, None] = None):
    words = preprocess(query)
    possible_documents = []
    invIdxDf = InvertedIndex()
    invIdxDf.load(input)
    def get_documents(word, encoding):
        if encoding is None:
            return set(invIdxDf.inv_idx.get(word, []))
        elif encoding == 'delta':
            cumsum_idx = np.cumsum([decode_delta_single(enc) for enc in invIdxDf.inv_idx_delta.get(word, [])])
            return set(cumsum_idx)
        elif encoding == 'gamma':
            cumsum_idx = np.cumsum([decode_gamma_single(enc) for enc in invIdxDf.inv_idx_gamma.get(word, [])])
            return set(cumsum_idx)
        return set()

    for word in words:
        possible_documents.append(get_documents(word, encoding))

    if not possible_documents or all(not docs for docs in possible_documents):
        return 'There are no related documents'

    intersection = set.intersection(*filter(None, possible_documents))

    if not intersection:
        return 'There are no related documents'

    return invIdxDf.df.loc[list(intersection)]

def main():
    parser = argparse.ArgumentParser(description='Search in prebuilt index')
    parser.add_argument('index', help='Path to index file')
    parser.add_argument('query', help='Search query')
    parser.add_argument('-e', '--encoding', 
                      choices=['delta', 'gamma', None],
                      default=None,
                      help='Encoding type')
    
    args = parser.parse_args()
    
    index_data = InvertedIndex.load(args.index)
    results = search(index_data, args.query, args.encoding)
    
    if isinstance(results, str):
        print(results)
    else:
        print(results.to_string(index=False))

if __name__ == "__main__":
    main()