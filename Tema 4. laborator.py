import random

# 1. Lista de cuvinte și alegerea cuvântului la întâmplare
cuvinte = ["calul", "masinarie", "bomboclat", "educatie", "procedura"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]

incercari_ramase = 6
litere_incercate = []

print("Cuvânt de ghicit: ", " ".join(progres))

while incercari_ramase > 0 and "_" in progres:
    litera = input("Introdu o literă: ").lower()

    if len(litera) != 1 or not litera.isalpha():
        print("Te rog introdu o literă validă!")
        continue
    if litera in litere_incercate:
        print("Ai încercat deja această literă! Încearcă alta.")
        continue

    litere_incercate.append(litera)

    if litera in cuvant_de_ghicit:
        for i in range(len(cuvant_de_ghicit)):
            if cuvant_de_ghicit[i] == litera:
                progres[i] = litera
        print("Corect!")
    else:
        incercari_ramase -= 1
        print("Litera nu se află în cuvânt. Încercări rămase:", incercari_ramase)

    print("Progresul curent:", " ".join(progres))
    print("Litere încercate:", ", ".join(litere_incercate))

if "_" not in progres:
    print("Felicitări! Ai ghicit cuvântul:", cuvant_de_ghicit)
else:
    print("Ai pierdut! Cuvântul era:", cuvant_de_ghicit)