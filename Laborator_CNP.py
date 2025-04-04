import random
import csv
import datetime
import sys
import os


prenume_list = ["Ana", "Ion", "Maria", "George", "Elena", "Mihai", "Ioana", "Vasile", "Gabriela", "Andrei"]
nume_list = ["Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Marin", "Stoica", "Radu", "Petrescu", "Munteanu",
             "Constantinescu"]


def random_sex():

    return random.choice([1, 2])


def random_date():

    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date(2000, 12, 31)
    delta = (end_date - start_date).days
    random_day = random.randint(0, delta)
    d = start_date + datetime.timedelta(days=random_day)
    return d.year, d.month, d.day


def calc_control(cnp12):

    weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    s = sum(int(digit) * weight for digit, weight in zip(cnp12, weights))
    remainder = s % 11
    return remainder if remainder != 10 else 1


def generate_cnp():

    sex = random_sex()

    year, month, day = random_date()
    year_str = str(year)[-2:]
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"

    judet = random.randint(1, 52)
    judet_str = f"{judet:02d}"

    nnn = random.randint(1, 999)
    nnn_str = f"{nnn:03d}"

    cnp12 = f"{sex}{year_str}{month_str}{day_str}{judet_str}{nnn_str}"
    control = calc_control(cnp12)
    return cnp12 + str(control)


def generate_data_csv(filename="cnp_data.csv", total=1_000_000):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["CNP", "Nume"])
        for i in range(total):
            cnp = generate_cnp()
            prenume = random.choice(prenume_list)
            nume = random.choice(nume_list)
            full_name = f"{prenume} {nume}"
            writer.writerow([cnp, full_name])
            if (i + 1) % 100000 == 0:
                print(f"{i + 1} înregistrări generate...")
    print(f"\nFișierul {filename} a fost generat cu {total} înregistrări.")



class HashTable:
    def __init__(self, size=1000003):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):

        return sum(ord(ch) for ch in key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        iterations = 0
        for entry in self.table[index]:
            iterations += 1
            if entry[0] == key:
                return entry[1], iterations
        return None, iterations


def populate_hash_table(csv_filename="cnp_data.csv"):
    ht = HashTable()
    with open(csv_filename, mode="r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for i, row in enumerate(reader):
            cnp, full_name = row
            ht.insert(cnp, full_name)
            if (i + 1) % 100000 == 0:
                print(f"{i + 1} înregistrări inserate în hash table...")
    print("\nHash table populat cu cele 1.000.000 de înregistrări.")
    return ht


def random_searches(hash_table, csv_filename="cnp_data.csv", searches=1000):

    cnp_list = []
    with open(csv_filename, mode="r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            cnp_list.append(row[0])

    selected = random.sample(cnp_list, searches)
    total_iterations = 0
    found_count = 0

    for cnp in selected:
        value, iterations = hash_table.search(cnp)
        total_iterations += iterations
        if value is not None:
            found_count += 1

    average_iterations = total_iterations / searches
    print("\n--- Statistici Căutări ---")
    print(f"Căutări efectuate: {searches}")
    print(f"Număr total de iterații: {total_iterations}")
    print(f"Număr mediu de iterații pe căutare: {average_iterations:.2f}")



def main():
    csv_filename = "cnp_data.csv"
    total_records = 1_000_000


    if not os.path.exists(csv_filename):
        print("Generare fișier CSV...")
        generate_data_csv(csv_filename, total_records)
    else:
        print(f"Fișierul {csv_filename} există deja. Se va folosi fișierul existent.")


    ht = populate_hash_table(csv_filename)


    random_searches(ht, csv_filename, searches=1000)


if __name__ == '__main__':
    main()