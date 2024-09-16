def calculate_parity(bits):
    """Функция вычисления 3-битной функции от предыдущих 5 битов."""
    parity = 0
    for bit in bits:
        parity ^= bit  # XOR всех битов для чётности
    
    return parity & 0x7  # Оставляем только 3 младших бита

def encode_12bit_value(value):
    """Функция кодирования 12-битного значения в три 8-битных байта."""
    if value > 0xFFF:
        raise ValueError("Значение должно быть 12-битным (от 0 до 4095)")
    
    # Разбиваем 12-битное значение на три части по 4 бита
    parts = [(value >> 8) & 0xF, (value >> 4) & 0xF, value & 0xF]
    
    encoded_bytes = []
    
    for part in parts:
        # Формируем байт:
        # 1-бит проверки, 4 бита данных, 3 бита функции (чётности)
        byte = (1 << 7) | (part << 3)  # Первые 5 битов (1 + данные)
        
        # Вычисляем последние 3 бита функции
        first_5_bits = [(byte >> i) & 1 for i in range(7, 2, -1)]  # Разбиваем на отдельные биты
        print(f"Первые 5 бит для чётности: {first_5_bits}")  # Отладочный вывод
        parity = calculate_parity(first_5_bits)
        
        # Добавляем три бита функции (чётности)
        byte |= parity
        
        encoded_bytes.append(byte)
    
    return encoded_bytes

def decode_12bit_value(encoded_bytes):
    """Функция декодирования трёх 8-битных байтов в одно 12-битное значение."""
    if len(encoded_bytes) != 3:
        raise ValueError("Для декодирования требуется три байта")
    
    decoded_value = 0
    
    for i, byte in enumerate(encoded_bytes):
        # Проверяем первый бит (должен быть 1)
        if (byte >> 7) != 1:
            raise ValueError(f"Ошибка в структуре байта {i+1}: первый бит не равен 1")
        
        # Извлекаем полезные 4 бита данных
        data = (byte >> 3) & 0xF
        
        # Проверяем три последних бита функции
        first_5_bits = [(byte >> i) & 1 for i in range(7, 2, -1)]
        print(f"Первые 5 бит для чётности (декод): {first_5_bits}")  # Отладочный вывод
        parity = calculate_parity(first_5_bits)
        
        if (byte & 0x7) != parity:
            print(f"Ожидаемая чётность: {parity:03b}, полученная: {byte & 0x7:03b}")
            raise ValueError("Ошибка контрольной функции (чётности)")
        
        # Восстанавливаем 12-битное значение
        decoded_value |= (data << (8 - 4 * i))
    
    return decoded_value

def encode_data(data_list):
    """Функция для кодирования списка 12-битных значений в массив байтов."""
    encoded_bytes = []
    for value in data_list:
        encoded_bytes.extend(encode_12bit_value(value))
    return encoded_bytes

def decode_data(encoded_bytes):
    """Функция для декодирования массива байтов в список 12-битных значений."""
    decoded_data = []
    for i in range(0, len(encoded_bytes), 3):
        decoded_value = decode_12bit_value(encoded_bytes[i:i + 3])
        decoded_data.append(decoded_value)
    return decoded_data

# Пример использования:
data_list = [0x0F3, 0x57B, 0xA4D]  # Список 12-битных значений

# Кодирование данных
encoded_data = encode_data(data_list)
encoded_hex = " ".join([f"{byte:08b}" for byte in encoded_data])
print(f"Закодированные данные: {encoded_hex}")

# Декодирование данных
try:
    decoded_data = decode_data(encoded_data)
    decoded_hex = " ".join([f"{value:03X}" for value in decoded_data])
    print(f"Декодированные данные: {decoded_hex}")
except ValueError as e:
    print(f"Ошибка: {e}")
