import random
from itertools import combinations

# Функция для вычисления расстояния Хэмминга между двумя числами
def hamming_distance(a, b):
    return bin(a ^ b).count('1')

# Генерация кодовой книги с минимальным расстоянием Хэмминга 5
def generate_codebook(n_codewords=16, codeword_length=16, min_distance=5):
    codebook = []
    for codeword in range(0, 1 << codeword_length):
        # Проверяем расстояние Хэмминга до всех уже добавленных кодовых слов
        if all(hamming_distance(codeword, existing) >= min_distance for existing in codebook):
            codebook.append(codeword)
            if len(codebook) == n_codewords:
                break
    if len(codebook) < n_codewords:
        raise ValueError(f"Не удалось сгенерировать кодовую книгу из {n_codewords} кодовых слов с длиной {codeword_length} бит и минимальным расстоянием {min_distance}.")
    return codebook

# Создаём кодовую книгу
try:
    CODEBOOK_LIST = generate_codebook()
except ValueError as e:
    print(e)
    # В случае необходимости можно увеличить длину кодового слова или уменьшить минимальное расстояние
    exit(1)

# Создаём словарь для быстрого доступа: ниббл -> кодовое слово
CODEBOOK = {nibble: codeword for nibble, codeword in enumerate(CODEBOOK_LIST)}

# Проверка минимального расстояния Хэмминга
def verify_codebook(codebook, min_distance=5):
    codewords = list(codebook.values())
    for (i, cw1), (j, cw2) in combinations(enumerate(codewords), 2):
        distance = hamming_distance(cw1, cw2)
        if distance < min_distance:
            print(f"Расстояние Хэмминга между кодами {i} и {j} равно {distance}. Требуется минимум {min_distance}.")
            return False
    print(f"Кодовая книга прошла проверку на минимальное расстояние Хэмминга {min_distance}.")
    return True

# Верифицируем кодовую книгу
verify_codebook(CODEBOOK)

# Функция кодирования
def encode(nibble):
    return CODEBOOK[nibble]

# Функция введения ошибок (до 2 битов)
def introduce_errors(codeword, max_errors=2):
    num_errors = random.randint(0, max_errors)
    error_positions = random.sample(range(16), num_errors)
    for pos in error_positions:
        codeword ^= (1 << pos)
    return codeword

# Функция декодирования
def decode(received, codebook):
    min_distance = float('inf')
    decoded_nibble = None
    for nibble, codeword in codebook.items():
        distance = hamming_distance(received, codeword)
        if distance < min_distance:
            min_distance = distance
            decoded_nibble = nibble
            if min_distance == 0:
                break  # Найдено точное совпадение
    return decoded_nibble

# Пример работы с числами AF3, AD0, 13F
input_hex = ['FFF', 'AD0', '13F']

# Разбиваем 12-битные числа на три 4-битных ниббла
def split_into_nibbles(hex_number):
    # Преобразуем в целое число
    num = int(hex_number, 16)
    nibbles = []
    for shift in range(8, -4, -4):
        nibble = (num >> shift) & 0xF
        nibbles.append(nibble)
    return nibbles

# Обрабатываем каждое число
for hex_num in input_hex:
    print(f"\nИсходное число: {hex_num}")
    nibbles = split_into_nibbles(hex_num)
    print(f"Нибблы: {[hex(n) for n in nibbles]}")
    
    encoded = [encode(nibble) for nibble in nibbles]
    print("Закодированные 16-битные числа:")
    for e in encoded:
        print(f"{e:016b}")
    
    # Вводим ошибки
    corrupted = [introduce_errors(e) for e in encoded]
    print("Поврежденные 16-битные числа:")
    for c in corrupted:
        print(f"{c:016b}")
    
    # Декодируем
    decoded = [decode(c, CODEBOOK) for c in corrupted]
    print(f"Декодированные нибблы: {[hex(d) for d in decoded]}")
    
    # Собираем обратно 12-битное число
    decoded_num = 0
    for nibble in decoded:
        decoded_num = (decoded_num << 4) | nibble
    print(f"Восстановленное число: {hex(decoded_num)[2:].upper()}")

# Отображение Кодовой Книги
print("\nКодовая книга (Ниббл -> Кодовое слово):")
for nibble in range(16):
    print(f"0x{nibble:X} -> {CODEBOOK[nibble]:016b}")
