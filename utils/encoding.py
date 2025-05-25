def encode_delta_single(N: int) -> str:
    """ 
    Кодирование числа N с использованием алгоритма Элиаса дельта.
    Source link: https://en.wikipedia.org/wiki/Elias_delta_coding 
    """
    binary_N = bin(N)[2:]  # Пример: 10 -> '0b: [1010]'
    
    length_binary_N = len(binary_N)
    
    binary_length = bin(length_binary_N)[2:]
    
    M = len(binary_length)
    
    encoded = '0' * (M - 1) + '1' + binary_length[1:] + binary_N[1:]
    
    return encoded

def decode_delta_single(encoded: str) -> int:
    if len(encoded) == 1:
        return 1
    
    M = 0
    while M < len(encoded) and encoded[M] == '0':
        M += 1

    binary_length = len(encoded) - 2 * M - 1
    result = (1 << binary_length) + int(encoded[2 * M + 1:], 2)
    return result

def encode_gamma_single(N: int) -> str:
    """ 
    Source link: https://en.wikipedia.org/wiki/Elias_gamma_coding
    """
    N_bin = bin(N)[2:]
    length = len(N_bin) - 1
    result = '0' * length + N_bin
    
    return result

def decode_gamma_single(encoded: str) -> int:
    leading_zeros = encoded.find('1')

    number_binary = encoded[leading_zeros:]
    
    return int(number_binary, 2)