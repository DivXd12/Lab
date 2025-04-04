import hashlib
import string
import sys

# Funcția de criptare SHA-256
def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Parola criptată dată
target_hash = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"

# Seturile de caractere disponibile pentru fiecare categorie
uppercase_letters = list(string.ascii_uppercase)   # A-Z
lowercase_letters = list(string.ascii_lowercase)   # a-z
digits = list(string.digits)                         # 0-9
special_chars = list("!@#$")                         # caracterele speciale

# Variabilă globală pentru numărarea apelurilor recursive
recursive_calls = 0
found = False  # flag pentru a opri căutarea când se găsește parola

# Funcția de backtracking
def backtrack(current, counts):
    global recursive_calls, found
    recursive_calls += 1

    # Dacă s-au completat 6 caractere și toate categoriile sunt exact consumate
    if len(current) == 6:
        if all(v == 0 for v in counts.values()):
            candidate = "".join(current)
            if get_hash(candidate) == target_hash:
                print("Parola găsită:", candidate)
                print("Număr apeluri recursive:", recursive_calls)
                found = True
                sys.exit(0)  # Oprirea imediată a programului
        return

    # Dacă deja s-au completat 6 caractere, dar nu toate cerințele au fost îndeplinite, revenim
    # Parcurgem fiecare categorie ce încă mai poate fi folosită
    for category, available in counts.items():
        if available > 0:
            # Alege lista de caractere corespunzătoare categoriei
            if category == "upper":
                chars = uppercase_letters
            elif category == "lower":
                chars = lowercase_letters
            elif category == "digit":
                chars = digits
            elif category == "special":
                chars = special_chars
            else:
                continue

            # Pentru fiecare caracter din categoria respectivă
            for ch in chars:
                current.append(ch)
                counts[category] -= 1

                backtrack(current, counts)

                # Backtracking: revenim la configurația anterioară
                counts[category] += 1
                current.pop()

# Inițializarea contorilor pentru fiecare categorie:
# 1 literă mare, 3 litere mici, 1 cifră și 1 caracter special
initial_counts = {
    "upper": 1,
    "lower": 3,
    "digit": 1,
    "special": 1
}

# Pornirea backtracking-ului
backtrack([], initial_counts)

# Dacă se termină căutarea fără a găsi parola, se afișează un mesaj
if not found:
    print("Nu s-a găsit nicio parolă care să corespundă.")