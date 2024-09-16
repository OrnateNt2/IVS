import random
from itertools import combinations

# Функция для вычисления расстояния Хэмминга между двумя числами
def hamming_distance(a, b):
    return bin(a ^ b).count('1')

# Новая кодовая книга для 4-битных чисел, закодированных в 32-битные слова
# Кодовая книга гарантирует расстояние Хэмминга >= 7
CODEBOOK = {
    0x0: 0b00000000000000000000000000000000,
    0x1: 0b11111111000000000000000000000000,
    0x2: 0b00000000111111110000000000000000,
    0x3: 0b00000000000000001111111100000000,
    0x4: 0b11110000111100001111000011110000,
    0x5: 0b00001111000011110000111100001111,
    0x6: 0b11111111111100000000000011111111,
    0x7: 0b00000000111111111111111100000000,
    0x8: 0b11001100110011001100110011001100,
    0x9: 0b10101010101010101010101010101010,
    0xA: 0b01010101010101010101010101010101,
    0xB: 0b11111111111111110000000000000000,
    0xC: 0b00000000000000001111111111111111,
    0xD: 0b11110000111100001111000000001111,
    0xE: 0b11000011110000111100001111000011,
    0xF: 0b11111111111111111111111100000000
}

# Проверка минимального расстояния Хэмминга в кодовой книге
def verify_codebook(codebook, min_distance=7):
    codewords = list(codebook.values())
    for (i, cw1), (j, cw2) in combinations(enumerate(codewords), 2):
        distance = hamming_distance(cw1, cw2)
        if distance < min_distance:
            print(f"Расстояние Хэмминга между кодами {hex(i)} и {hex(j)} равно {distance}. Требуется минимум {min_distance}.")
            return False
    print(f"Кодовая книга прошла проверку на минимальное расстояние Хэмминга {min_distance}.")
    return True

# Проверим, что наша кодовая книга имеет минимальное расстояние Хэмминга 7
verify_codebook(CODEBOOK)

# Функция кодирования
def encode(nibble):
    return CODEBOOK[nibble]

# Функция инверсии до 2 бит в каждом байте
def invert_bits(byte, num_bits=2):
    positions = random.sample(range(8), num_bits)
    for pos in positions:
        byte ^= (1 << pos)
    return byte

# Функция для введения ошибок: инвертируем по 2 бита в каждом из четырёх байтов
def introduce_errors(codeword):
    byte1 = (codeword >> 24) & 0xFF
    byte2 = (codeword >> 16) & 0xFF
    byte3 = (codeword >> 8) & 0xFF
    byte4 = codeword & 0xFF

    byte1 = invert_bits(byte1, 2)
    byte2 = invert_bits(byte2, 2)
    byte3 = invert_bits(byte3, 2)
    byte4 = invert_bits(byte4, 2)

    # Собираем обратно поврежденное слово
    corrupted = (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4
    return corrupted

# Функция декодирования (ищем ближайшее кодовое слово по расстоянию Хэмминга)
def decode(received, codebook):
    min_distance = float('inf')
    decoded_nibble = None
    for nibble, codeword in codebook.items():
        distance = hamming_distance(received, codeword)
        if distance < min_distance:
            min_distance = distance
            decoded_nibble = nibble
            if min_distance == 0:
                break  # Нашли точное совпадение
    return decoded_nibble

# Функция для форматирования 32-битного слова с разделением по 8 бит
def format_32bit_word(word):
    return f'{(word >> 24) & 0xFF:08b} {(word >> 16) & 0xFF:08b} {(word >> 8) & 0xFF:08b} {word & 0xFF:08b}'

# Пример работы с числами 0xA, 0xF, 0x3
input_nibbles = [0xA, 0xF, 0x3]

# Кодируем и декодируем каждое число
for nibble in input_nibbles:
    print(f"\nИсходное 4-битное число: {hex(nibble)}")
    
    # Кодируем в 32-битное слово
    encoded = encode(nibble)
    print(f"Закодированное 32-битное слово: {format_32bit_word(encoded)}")

    # Вводим ошибки
    corrupted = introduce_errors(encoded)
    print(f"Поврежденное 32-битное слово: {format_32bit_word(corrupted)}")

    # Декодируем поврежденное слово
    decoded = decode(corrupted, CODEBOOK)
    print(f"Декодированное 4-битное число: {hex(decoded)}")
