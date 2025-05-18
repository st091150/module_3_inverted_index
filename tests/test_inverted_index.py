import pytest
import time
from main import InvertedIndex
from utils import encode_delta_single, decode_delta_single, encode_gamma_single, decode_gamma_single


@pytest.fixture(scope="module")
def index():
    inv_idx = InvertedIndex()
    inv_idx.merge_jsons(["./data/test.json"])
    inv_idx.get_inverted_index()
    inv_idx.encode_delta()
    inv_idx.encode_gamma()
    return inv_idx


def test_basic_search(index):
    df = index.find("ректор СПбГУ")
    assert len(df) == 2
    assert all("ректор" in row["message"].lower() for _, row in df.iterrows())

def test_search_single_word(index):
    df = index.find("форуме")
    assert len(df) == 1
    assert "форуме" in df.iloc[0]['message'].lower()

def test_search_multiple_results(index):
    df = index.find("СПбГУ")
    assert len(df) == 4

def test_search_mgu(index):
    df = index.find("МГУ")
    assert len(df) == 2

def test_search_with_delta(index):
    df = index.find("ректор СПбГУ", encoding="delta")
    assert len(df) == 2

def test_search_with_gamma(index):
    df = index.find("ректор СПбГУ", encoding="gamma")
    assert len(df) == 2

def test_nonexistent_term(index):
    result = index.find("Гарри Поттер")
    assert result == "There are no related documents"

def test_case_insensitivity(index):
    df1 = index.find("спбгу")
    df2 = index.find("СПБГУ")
    assert df1.equals(df2)

def test_index_keys(index):
    assert "спбгу" in index.inv_idx
    assert "ректор" in index.inv_idx

def test_performance_of_search(index):
    start = time.time()
    result = index.find("СПбГУ", encoding="gamma")
    duration = time.time() - start
    assert duration < 1.0, f"Search took too long: {duration} seconds"
    assert isinstance(result, object)


def test_storage_efficiency(index):
    word = "спбгу"
    uncompressed = len(index.inv_idx[word])
    delta_size = sum(len(code) for code in index.inv_idx_delta[word])
    gamma_size = sum(len(code) for code in index.inv_idx_gamma[word])
    assert delta_size < uncompressed * 10  # проверка что сжатие работает
    assert gamma_size < uncompressed * 10


def test_delta_encoding_correctness():
    numbers = [1, 3, 7, 15]
    encoded = [encode_delta_single(n) for n in numbers]
    decoded = [decode_delta_single(e) for e in encoded]
    assert decoded == numbers


def test_gamma_encoding_correctness():
    numbers = [1, 3, 7, 15]
    encoded = [encode_gamma_single(n) for n in numbers]
    decoded = [decode_gamma_single(e) for e in encoded]
    assert decoded == numbers
