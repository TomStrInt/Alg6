#!/usr/bin/env python3


#Prosta funkcja haszująca, która:
#Sumuje kody ASCII wszystkich znaków w podanym ciągu s.
#Zwraca sumę modulo 'table_size', co daje indeks w tablicy.


def simple_hash(s: str, table_size: int):

    return sum(ord(char) for char in s) % table_size


def horner_hash(s: str, table_size: int) -> int:
    hash_value = 0
    base = 31
    for char in s:
        hash_value = (hash_value * base + ord(char)) % table_size
    return hash_value


def djb2_hash(s: str, table_size: int) -> int:
    hash_value = 5381
    for char in s:
        hash_value = ((hash_value * 33) + ord(char)) % table_size
    return hash_value

#IMPLEMENTACJA PROSTEJ HASHMAPY

class HashMap:

    def __init__(self, table_size: int, hash_func):
        self.table_size = table_size
        self.table = [[] for _ in range(table_size)]
        self.hash_func = hash_func

    def put(self, key: str, value):
        index = self.hash_func(key, self.table_size)
        # Jeśli klucz już istnieje, aktualizujemy wartość
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key: str):
        index = self.hash_func(key, self.table_size)
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(f"Klucz '{key}' nie został znaleziony.")

    def __getitem__(self, key: str):
        return self.get(key)

    def __setitem__(self, key: str, value):
        self.put(key, value)

    def __repr__(self):
        output = "HashMap:\n"
        for i, bucket in enumerate(self.table):
            output += f"  Bucket {i} -> {bucket}\n"
        return output

# --- FUNKCJE POMOCNICZE DO PREZENTACJI WYNIKÓW ---

def print_comparison_table(keys, table_size):
    """
    Funkcja wypisuje tabelkę, w której dla każdego klucza pokazane są wyniki
    uzyskane przez każdą z trzech funkcji haszujących.
    """
    header = f"{'Klucz':15} | {'Simple':6} | {'Horner':6} | {'DJB2':6}"
    print(header)
    print("-" * len(header))
    
    for key in keys:
        sh = simple_hash(key, table_size)
        hh = horner_hash(key, table_size)
        dj = djb2_hash(key, table_size)
        print(f"{key:15} | {sh:6} | {hh:6} | {dj:6}")
    print()


def compute_distribution(hash_func, keys, table_size):
    """
    Funkcja tworzy dystrybucję (rozklad) kluczy w koszykach (bucketach)
    przy użyciu danej funkcji haszującej. Zwraca słownik, w którym:
      - Klucz: indeks bucketu,
      - Wartość: lista kluczy, które zmapowały się na ten bucket.
    """
    distribution = {i: [] for i in range(table_size)}
    for key in keys:
        idx = hash_func(key, table_size)
        distribution[idx].append(key)
    return distribution


def print_distribution_table(distribution, func_name: str):
    """
    Wypisuje tabelarycznie rozkład kluczy w bucketach.
    """
    print(f"Rozkład kluczy dla funkcji {func_name}:")
    print(f"{'Bucket':6} | {'Ilość':5} | {'Klucze'}")
    print("-" * 40)
    for bucket in sorted(distribution.keys()):
        keys_in_bucket = ", ".join(distribution[bucket])
        print(f"{bucket:6} | {len(distribution[bucket]):5} | {keys_in_bucket}")
    print()


# --- PRZYKŁADOWE DANE I DEMONSTRACJA ---

if __name__ == "__main__":
    # Ustalamy rozmiar tablicy (np. 10 bucketów)
    table_size = 10

    # Generujemy listę 25 podobnych stringów
    keys = [f"klucz{i}" for i in range(1, 26)]
    
    # 1. Tabela porównawcza hashy dla każdego klucza
    print("Tabela porównawcza wyników haszujących:")
    print_comparison_table(keys, table_size)
    
    # 2. Obliczamy i wypisujemy rozkład (dystrybucję) dla każdej funkcji
    
    # Rozkład dla prostej funkcji simple_hash
    dist_simple = compute_distribution(simple_hash, keys, table_size)
    print_distribution_table(dist_simple, "simple_hash")
    
    # Rozkład dla funkcji horner_hash
    dist_horner = compute_distribution(horner_hash, keys, table_size)
    print_distribution_table(dist_horner, "horner_hash")
    
    # Rozkład dla funkcji djb2_hash
    dist_djb2 = compute_distribution(djb2_hash, keys, table_size)
    print_distribution_table(dist_djb2, "djb2_hash")
    
    # 3. Przykład użycia HashMap z prosta funkcją haszującą (simple_hash)
    hashmap = HashMap(table_size, simple_hash)
    for key in keys:
        # W HashMap możemy przechować dowolne wartości - tu używamy przykładowej wartości równiej długości klucza
        hashmap[key] = len(key)
    
    print("Przykładowa HashMap (z użyciem simple_hash):")
    print(hashmap)
