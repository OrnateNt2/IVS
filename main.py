def calculate_parity(bits):
    """Функция вычисления двух бит чётности от первых 6 битов."""
    parity = 0
    for bit in bits:
        parity ^= bit  # XOR всех битов
    
    return (parity & 0x3)  # Оставляем только 2 младших бита

def encode_byte(data):
    """Формирует один байт по указанной структуре."""
    if data > 0xF:
        raise ValueError("Полезная информация должна быть 4-битной (от 0 до 15)")
    
    # Структура байта:
    # 1-бит проверки, 4 бита данных, 1-бит проверки (0), 2 бита функции (чётности)
    byte = (1 << 7) | (data << 2) | (0 << 1)  # Первые 6 битов (1 + данные + 0)
    
    # Вычисляем последние 2 бита функции
    first_6_bits = [(byte >> i) & 1 for i in range(5, -1, -1)]  # Разбиваем на отдельные биты
    parity = calculate_parity(first_6_bits)
    
    # Добавляем два бита функции (чётности)
    byte |= parity
    
    return byte

def decode_byte(byte):
    """Разбирает байт и проверяет его корректность."""
    # Проверяем первый бит (должен быть 1) и шестой (должен быть 0)
    if (byte >> 7) != 1 or ((byte >> 1) & 1) != 0:
        raise ValueError("Ошибка в структуре байта (проверочные биты)")
    
    # Извлекаем полезные 4 бита данных
    data = (byte >> 2) & 0xF
    
    # Проверяем два последних бита функции
    first_6_bits = [(byte >> i) & 1 for i in range(5, -1, -1)]
    parity = calculate_parity(first_6_bits)
    if (byte & 0x3) != parity:
        raise ValueError("Ошибка контрольной функции (чётности)")
    
    return data

# Пример использования
encoded = encode_byte(0xA)  # Кодируем 4-битное число (например, 0xA = 1010)
print(f"Закодированный байт: {encoded:08b}")

try:
    decoded = decode_byte(encoded)  # Декодируем байт
    print(f"Декодированное число: {decoded:01X}")
except ValueError as e:
    print(f"Ошибка: {e}")
