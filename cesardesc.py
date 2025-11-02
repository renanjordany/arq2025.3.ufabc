import sys
import random
import time
from math import log10

class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        print(f"Carregando n-grams '{ngramfile}'...")
        print("Aguarde...")
        self.ngrams = {}
        try:
            with open(ngramfile, encoding='utf-8') as f:
                for line in f:
                    try:
                        key, count = line.split(sep)
                        self.ngrams[key] = int(count)
                    except ValueError:
                        continue
        except FileNotFoundError:
            print(f"Arquivo de n-grams '{ngramfile}' não encontrado.")
            sys.exit()

        if not self.ngrams:
            print(f"Nenhum n-gram carregado de '{ngramfile}'.")
            sys.exit()

        self.L = len(next(iter(self.ngrams.keys())))
        self.N = sum(self.ngrams.values())

        for k in list(self.ngrams.keys()):
            self.ngrams[k] = log10(float(self.ngrams[k]) / self.N)

        self.floor = log10(0.01 / self.N)
        print("N-grams prontos.\n")

    def score(self, text):
        clean_text = "".join(c for c in text.upper() if 'A' <= c <= 'Z')
        if len(clean_text) < self.L:
            return self.floor * len(text)
        s = 0
        getng = self.ngrams.__getitem__
        for i in range(len(clean_text) - self.L + 1):
            gram = clean_text[i:i + self.L]
            if gram in self.ngrams:
                s += getng(gram)
            else:
                s += self.floor
        return s

def bin_to_text(binary_data):
    try:
        return ''.join(chr(int(b, 2)) for b in binary_data.split())
    except Exception as e:
        print("Erro na conversão binária:", e)
        sys.exit()

def caesar_decrypt(ciphertext, shift):
    out = []
    for ch in ciphertext:
        if 'A' <= ch <= 'Z':
            n = ord(ch) - shift
            if n < ord('A'):
                n += 26
            out.append(chr(n))
        else:
            out.append(ch)
    return ''.join(out)

def attack_caesar(ciphertext, fitness):
    print("\n--- Ataque: César ---")
    start = time.time()
    best_score = -float('inf')
    best_key = 0
    best_text = ""
    for k in range(26):
        attempt = caesar_decrypt(ciphertext, k)
        sc = fitness.score(attempt)
        if sc > best_score:
            best_score = sc
            best_key = k
            best_text = attempt
    elapsed = time.time() - start
    print("\nResultado (César):")
    print(f"Tempo: {elapsed:.4f}s")
    print(f"Chave: {best_key}")
    print(f"Score: {best_score:.2f}\n")
    print(best_text)
    print("\n(Nota: saída ilegível indica cifra de substituição.)")

def substitution_decrypt(ciphertext, key_map):
    out = []
    for ch in ciphertext.upper():
        out.append(key_map.get(ch, ch))
    return ''.join(out)

def create_key_map(key_string):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {alphabet[i]: key_string[i] for i in range(26)}

def attack_substitution(ciphertext, fitness):
    print("\n--- Ataque: Substituição (Hill Climb) ---")
    start = time.time()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_list = list(alphabet)
    random.shuffle(key_list)
    best_key_str = "".join(key_list)
    best_map = create_key_map(best_key_str)
    best_plaintext = substitution_decrypt(ciphertext, best_map)
    best_score = fitness.score(best_plaintext)
    print(f"Score inicial: {best_score:.2f}")
    it_no_imp = 0
    max_iter = 10000

    for i in range(max_iter):
        new_key_list = list(best_key_str)
        p1, p2 = random.sample(range(26), 2)
        new_key_list[p1], new_key_list[p2] = new_key_list[p2], new_key_list[p1]
        new_key_str = "".join(new_key_list)
        new_map = create_key_map(new_key_str)
        new_plain = substitution_decrypt(ciphertext, new_map)
        new_score = fitness.score(new_plain)

        if new_score > best_score:
            best_score = new_score
            best_key_str = new_key_str
            best_plaintext = new_plain
            it_no_imp = 0
            print(f"Iter {i} | Novo melhor: {best_score:.2f} | {best_plaintext[:60]}...")
        else:
            it_no_imp += 1

        if it_no_imp >= 1000:
            tmp = list(alphabet)
            random.shuffle(tmp)
            best_key_str = "".join(tmp)
            it_no_imp = 0

    elapsed = time.time() - start
    print("\nResultado (Substituição):")
    print(f"Tempo: {elapsed:.4f}s")
    print(f"Chave: {best_key_str}")
    print(f"Score: {best_score:.2f}\n")
    print(best_plaintext)

def main():
    print(r"""
  __  __                  _       _       _      ____                   _              
 |  \/  | ___  _ __     ___| | __ _| |_ ___| |__    |  _ \ ___  ___ __ _| | ___  _ __   
 | |\/| |/ _ \| '_ \   / _ \ |/ _` | __/ __| '_ \   | |_) / _ \/ __/ _` |/ _ \| '__|  
 | |  | | (_) | | | | |  __/ | (_| | || (__| | | |  |  _ <  __/ (_| (_| | (_) | |     
 |_|  |_|\___/|_| |_|  \___|_|\__,_|\__\___|_| |_|  |_| \_\___|\___\__,_|\___/|_|     

              Menino da Porteira - O Decifrador Supremo
    """)

    filename_encoded = input("Arquivo codificado (ex: encoded.txt): ")
    try:
        with open(filename_encoded, 'r') as f:
            binary_data = f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        sys.exit()

    ciphertext = bin_to_text(binary_data)
    print(f"Arquivo '{filename_encoded}' lido e convertido.")

    try:
        fitness = ngram_score('quadgrams.txt')
    except Exception as e:
        print("Erro ao carregar quadgrams:", e)
        sys.exit()

    while True:
        print("\n" + "="*30)
        print(" MENU ")
        print("="*30)
        print("1. Cifra de César")
        print("2. Substituição (Hill Climb)")
        print("3. Sair")
        choice = input("Opção: ").strip()
        if choice == '1':
            attack_caesar(ciphertext, fitness)
        elif choice == '2':
            attack_substitution(ciphertext, fitness)
        elif choice == '3':
            print("Tchau!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

