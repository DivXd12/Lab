import hashlib
import string
import sys


def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


target_hash = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"


uppercase_letters = list(string.ascii_uppercase)
lowercase_letters = list(string.ascii_lowercase)
digits = list(string.digits)
special_chars = list("!@#$")


recursive_calls = 0
found = False

# Funcția de backtracking
def backtrack(current, counts):
    global recursive_calls, found
    recursive_calls += 1


    if len(current) == 6:
        if all(v == 0 for v in counts.values()):
            candidate = "".join(current)
            if get_hash(candidate) == target_hash:
                print("Parola găsită:", candidate)
                print("Număr apeluri recursive:", recursive_calls)
                found = True
                sys.exit(0)
        return


    for category, available in counts.items():
        if available > 0:

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


            for ch in chars:
                current.append(ch)
                counts[category] -= 1

                backtrack(current, counts)


                counts[category] += 1
                current.pop()


initial_counts = {
    "upper": 1,
    "lower": 3,
    "digit": 1,
    "special": 1
}


backtrack([], initial_counts)


if not found:
    print("Nu s-a găsit nicio parolă care să corespundă.")