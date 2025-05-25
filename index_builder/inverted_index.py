import pandas as pd
import numpy as np
import pickle
from collections import defaultdict
from typing import Callable, List

from utils.encoding import *
from utils.utils import preprocess

class InvertedIndex:
    def __init__(self):
        self.columns_to_keep = ['date', 'message']
        self.df = pd.DataFrame()
        self.inv_idx = defaultdict(list)
        self.inv_idx_delta = defaultdict(list)
        self.inv_idx_gamma = defaultdict(list)

    def merge_jsons(self, paths):
        if not paths:
            raise ValueError("Empty paths!")
        
        list_df = [
            pd.read_json(path)[self.columns_to_keep]
            for path in paths
        ]
        self.df = pd.concat(list_df, ignore_index=True).dropna(subset=['message'])

    def build_index(self):
        for idx, row in self.df.iterrows():
            words = preprocess(row['message'])
            for word in words:
                self.inv_idx[word].append(idx)
        
        for k, v in self.inv_idx.items():
            self.inv_idx[k] = sorted(list(set(v)))

    def encode_indexes(self):
        self._base_encode(encode_delta_single, self.inv_idx_delta)
        self._base_encode(encode_gamma_single, self.inv_idx_gamma)

    def _base_encode(self, encode_func : Callable, inv_idx_list : List):
        for word, list_idx in self.inv_idx.items():
            diff = [list_idx[0]]
            diff.extend(list(np.diff(list_idx)))

            encoded = [encode_func(number) for number in diff]
            inv_idx_list[word] = encoded
            
    def load(self, input_path):
        with open(input_path, 'rb') as f:
            data = pickle.load(f)
        self.df = data['df']
        self.inv_idx = data['inv_idx']
        self.inv_idx_delta = data['inv_idx_delta']
        self.inv_idx_gamma = data['inv_idx_gamma']

    def save(self, output_path):
        with open(output_path, 'wb') as f:
            pickle.dump({
                'df': self.df,
                'inv_idx': self.inv_idx,
                'inv_idx_delta': self.inv_idx_delta,
                'inv_idx_gamma': self.inv_idx_gamma
            }, f)