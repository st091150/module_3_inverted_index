import re
import pandas as pd
import numpy as np
from typing import Callable, List

from collections import defaultdict
from bitstring import BitArray

from utils import encode_delta_single, encode_gamma_single, decode_delta_single, decode_gamma_single


class InvertedIndex:
    def __init__(self):
        self.columns_to_keep = ['date', 'message']
        self.list_df = []
        self.df = None
        self.inv_idx = defaultdict(list)
        self.inv_idx_delta = defaultdict(list)
        self.inv_idx_gamma = defaultdict(list)


    def merge_jsons(self, paths):
        if not paths:
            raise ValueError("Empty paths!")
    
        self.list_df = [
            pd.read_json(path)[self.columns_to_keep]
            for path in paths
        ]
        
        self.df = pd.concat(self.list_df, ignore_index=True).dropna(subset=['message'])


    def preprocess(self, message):
        """ Remove punctuation, cast to lower case and split the message """
        cleaned_message = re.sub(r'\W+', ' ', message.lower())
        return set(cleaned_message.split())


    def get_inverted_index(self):
        for idx, row in self.df.iterrows():
            words = self.preprocess(row['message'])
            for word in words:
                self.inv_idx[word].append(idx)

        for k, v in self.inv_idx.items():
            self.inv_idx[k] = sorted(list(set(v)))


    def reset_inv_idx(self):
        self.inv_idx = defaultdict(list)
        self.inv_idx_delta = defaultdict(list)
        self.inv_idx_gamma = defaultdict(list)

    def base_encode(self, encode_func : Callable, inv_idx_list : List):
        for word, list_idx in self.inv_idx.items():
            diff = [list_idx[0]]
            diff.extend(list(np.diff(list_idx)))

            encoded = [encode_func(number) for number in diff]
            inv_idx_list[word] = encoded

    def encode_delta(self):
        self.base_encode(encode_delta_single, self.inv_idx_delta)

    def encode_gamma(self):
        self.base_encode(encode_gamma_single, self.inv_idx_gamma)


    def find(self, text, encoding=None):
        words = self.preprocess(text)
        possible_documents = []

        def get_documents(word, encoding):
            if encoding is None:
                return set(self.inv_idx.get(word, []))
            elif encoding == 'delta':
                cumsum_idx = np.cumsum([decode_delta_single(enc) for enc in self.inv_idx_delta.get(word, [])])
                return set(cumsum_idx)
            elif encoding == 'gamma':
                cumsum_idx = np.cumsum([decode_gamma_single(enc) for enc in self.inv_idx_gamma.get(word, [])])
                return set(cumsum_idx)
            return set()

        for word in words:
            possible_documents.append(get_documents(word, encoding))

        if not possible_documents or all(not docs for docs in possible_documents):
            return 'There are no related documents'

        intersection = set.intersection(*filter(None, possible_documents))

        if not intersection:
            return 'There are no related documents'

        return self.df.loc[list(intersection)]
