def calculate_hash(string: str, base: int, prime: int, length: int) -> int:
    hash_value = 0
    for index in range(length):
        hash_value = (base * hash_value + ord(string[index])) % prime
    return hash_value


def calculate_power_value(base: int, prime: int, pattern_length: int) -> int:
    power = 1
    for _ in range(pattern_length - 1):
        power = (power * base) % prime
    return power


def update_hash(prev_hash: int, base: int, prime: int, power: int, old_char: str, new_char: str) -> int:
    new_hash = (base * (prev_hash - ord(old_char) * power) + ord(new_char)) % prime
    if new_hash < 0:
        new_hash += prime
    return new_hash


def verify_match(text: str, pattern: str, start_pos: int) -> bool:
    for index in range(len(pattern)):
        if text[start_pos + index] != pattern[index]:
            return False
    return True


def rabin_karp(text: str, pattern: str) -> list[int]:
    if not pattern or not text or len(pattern) > len(text):
        return []
    
    base = 256  # Number of possible values in a byte
    prime = 101  # A prime number for hash calculation
    
    text_length = len(text)
    pattern_length = len(pattern)
    match_positions: list[int] = []
    
    # Calculate base^(pattern_length-1) % prime for rolling hash
    power = calculate_power_value(base, prime, pattern_length)
    
    pattern_hash = calculate_hash(pattern, base, prime, pattern_length)
    text_window_hash = calculate_hash(text, base, prime, pattern_length)
    
    for window_start in range(text_length - pattern_length + 1):
        if pattern_hash == text_window_hash and verify_match(text, pattern, window_start):
            match_positions.append(window_start)
        
        if window_start < text_length - pattern_length:
            text_window_hash = update_hash(
                text_window_hash, 
                base, 
                prime, 
                power, 
                text[window_start], 
                text[window_start + pattern_length]
            )
    
    return match_positions
