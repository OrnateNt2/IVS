import random

# Count different bits between two numbers
def diff(a, b):
    a_bits = bin(a)[2:].zfill(32)  # Convert to binary with leading zeros
    b_bits = bin(b)[2:].zfill(32)
    d = 0
    for x, y in zip(a_bits, b_bits):  # Compare bit by bit
        if x != y:
            d += 1
    return d

# Simple codebook
CODES = {
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

# Check the codebook
def check(book, min_dist=7):
    keys = list(book.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if diff(book[keys[i]], book[keys[j]]) < min_dist:
                print(f"Error: {keys[i]} vs {keys[j]} is too close")
                return False
    print(f"All codes are OK, min distance {min_dist}")
    return True

# Encode a nibble
def enc(nib):
    return CODES.get(nib)

# Flip random bits
def flip(byte, bits=2):
    for _ in range(bits):
        bit = random.randint(0, 7)
        byte ^= (1 << bit)
    return byte

# Corrupt the codeword
def corrupt(word):
    bytes_list = [(word >> shift) & 0xFF for shift in (24, 16, 8, 0)]
    for i in range(4):
        bytes_list[i] = flip(bytes_list[i], 2)
    return (bytes_list[0] << 24) | (bytes_list[1] << 16) | (bytes_list[2] << 8) | bytes_list[3]

# Decode a word
def dec(word, book):
    best = None
    best_dist = None
    for nib, code in book.items():
        d = diff(word, code)
        if best_dist is None or d < best_dist:
            best_dist = d
            best = nib
    return best

# Example
inputs = ['1010', '1111', '0011', '11', '0', '101', '1011']

for nib_str in inputs:
    if len(nib_str) != 4:
        print(f"Skipping {nib_str}, not 4 bits")
        continue
    nib = int(nib_str, 2)
    print(f"\nOriginal: {nib_str}")

    encoded = enc(nib)
    if encoded is None:
        print(f"Not found in codebook!")
        continue

    print(f"Encoded: {bin(encoded)}")

    corrupted = corrupt(encoded)
    print(f"Corrupted: {bin(corrupted)}")

    decoded = dec(corrupted, CODES)
    if decoded is not None:
        print(f"Decoded: {bin(decoded)[2:].zfill(4)}")
    else:
        print("Decode error!")
