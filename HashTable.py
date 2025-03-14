import csv
import random
import datetime

# --- Etapa 1: Generarea datelor ---

def generate_cnp(sex, year, month, day, county_code, sequence_number):
    """Generates a valid CNP based on provided parameters."""
    year_short = str(year % 100).zfill(2)
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    county_code_str = str(county_code).zfill(2)
    sequence_str = str(sequence_number).zfill(3)

    cnp_prefix = str(sex) + year_short + month_str + day_str + county_code_str + sequence_str

    control_digit = calculate_control_digit(cnp_prefix)
    return cnp_prefix + str(control_digit)

def calculate_control_digit(cnp_prefix):
    """Calculates the control digit for a CNP."""
    control_key = "279146358279"
    sum_val = 0
    for i in range(12):
        sum_val += int(cnp_prefix[i]) * int(control_key[i])
    remainder = sum_val % 11
    if remainder == 10:
        return 1
    return remainder

def is_valid_cnp(cnp):
    """Checks if a CNP is valid based on length and control digit."""
    if len(cnp) != 13 or not cnp.isdigit():
        return False
    prefix = cnp[:12]
    control_digit = int(cnp[12])
    return calculate_control_digit(prefix) == control_digit

def generate_date_of_birth(age_group):
    """Generates a random date of birth within a given age group.
    For simplicity, let's define age groups roughly."""
    current_year = datetime.datetime.now().year
    if age_group == "young": # 18-35
        start_year = current_year - 35
        end_year = current_year - 18
    elif age_group == "middle": # 36-55
        start_year = current_year - 55
        end_year = current_year - 36
    elif age_group == "old": # 56+
        start_year = 1900 # Assuming people older than 56 starting from 1900 for simplification
        end_year = current_year - 56
    else: # Default middle age
        start_year = current_year - 50
        end_year = current_year - 40

    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28) # Keep it simpler, not checking days per month for example purposes
    return year, month, day

def generate_name(sex):
    """Generates a random name based on sex (using simplified name lists)."""
    male_first_names = ["Ion", "Gheorghe", "Vasile", "Marian", "Andrei", "Mihai", "Florin", "Daniel", "Cristian", "Adrian"]
    female_first_names = ["Maria", "Elena", "Cristina", "Ana", "Gabriela", "Ioana", "Andreea", "Daniela", "Alexandra", "Mihaela"]
    last_names = ["Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Avram", "Moldovan", "Rusu", "Marinescu", "Stan", "Dinu"]

    if sex == 1 or sex == 3 or sex == 5 or sex == 7: # Male
        first_name = random.choice(male_first_names)
    else: # Female - 2, 4, 6, 8
        first_name = random.choice(female_first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_data(num_cnps=1000000):
    """Generates CNPs and names and saves to CSV.
    Uses simplified distribution for demonstration."""

    county_codes = list(range(1, 43)) # Romanian county codes (1-42) + Bucharest (46)
    county_codes.append(46) # Adding Bucharest
    age_groups = ["young", "middle", "old"]
    sexes = [1, 2] # Male, Female (for simplification using just 19XX, 20XX)

    cnp_data = []
    for _ in range(num_cnps):
        sex = random.choice(sexes)
        age_group = random.choice(age_groups)
        year, month, day = generate_date_of_birth(age_group)
        county_code = random.choice(county_codes)
        sequence_number = random.randint(1, 999) # Simplified sequence

        # Adjust sex digit based on year (simplified for 1900-2099 range)
        if year >= 2000:
            if sex == 1: sex = 5
            else: sex = 6
        elif year < 1900: # Very old - unlikely but for completeness if using older ranges
             if sex == 1: sex = 7
             else: sex = 8
        # else stays 1 or 2 for 1900-1999


        cnp = generate_cnp(sex, year, month, day, county_code, sequence_number)
        name = generate_name(sex)
        cnp_data.append({"CNP": cnp, "Nume": name})

    return cnp_data


# Generate and save to CSV
num_cnps_to_generate = 1000000
generated_data = generate_data(num_cnps_to_generate)

csv_filename = "cnp_data.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['CNP', 'Nume']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(generated_data)

print(f"Fisierul CSV '{csv_filename}' a fost generat cu {num_cnps_to_generate} CNP-uri.")


# --- Etapa 2: Implementarea și popularea unui hash table ---

class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)] # Separate chaining using lists

    def hash_function(self, key):
        """Simple hash function: sum of digits modulo capacity."""
        key_str = str(key)
        hash_value = 0
        for digit in key_str:
            hash_value += int(digit)
        return hash_value % self.capacity

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        index = self.hash_function(key)
        bucket = self.table[index]
        bucket.append((key, value)) # Append as tuple: (key, value)

    def search(self, key):
        """Searches for a key in the hash table and returns the value and iterations."""
        index = self.hash_function(key)
        bucket = self.table[index]
        iterations = 0
        for k, v in bucket:
            iterations += 1
            if k == key:
                return v, iterations # Value found, return value and iterations
        return None, iterations # Key not found, return None and iterations count


# Popularea Hash Table
hash_table_capacity = 1000037 # Prime number slightly larger than 1 million for better distribution
hash_table = HashTable(hash_table_capacity)

for item in generated_data:
    hash_table.insert(item["CNP"], item["Nume"])

print("Hash table populated.")


# --- Etapa 3: Prezentarea rezultatelor statistice ---

num_searches = 1000
random_cnps_to_search = random.sample(generated_data, num_searches)

total_iterations = 0
found_count = 0

for item in random_cnps_to_search:
    cnp_to_find = item["CNP"]
    name_found, iterations = hash_table.search(cnp_to_find)
    total_iterations += iterations
    if name_found:
        found_count += 1
    else:
        print(f"CNP '{cnp_to_find}' not found in hash table (which should not happen for generated data).") # For debugging only

average_iterations = total_iterations / num_searches

print(f"\n--- Rezultate Statiscice Cautari ---")
print(f"Numar total de cautari: {num_searches}")
print(f"CNP-uri gasite: {found_count}")
print(f"Iteratii totale pentru cautari: {total_iterations}")
print(f"Iteratii medii per cautare: {average_iterations:.2f}")


# --- Interfață simplă de căutare ---

def search_cnp_interface():
    while True:
        cnp_to_search = input("\nIntroduceti CNP-ul pentru cautare (sau 'exit' pentru a iesi): ")
        if cnp_to_search.lower() == 'exit':
            break
        if not is_valid_cnp(cnp_to_search):
            print("CNP invalid. Va rugam introduceti un CNP valid.")
            continue

        name_found, iterations = hash_table.search(cnp_to_search)
        if name_found:
            print(f"CNP: {cnp_to_search} - Nume: {name_found} (Iteratii: {iterations})")
        else:
            print(f"CNP '{cnp_to_search}' nu a fost gasit in hash table.") # Should not happen with data generated here, but good for general case.

if __name__ == "__main__":
    print("\n--- Interfață Cautare CNP ---")
    search_cnp_interface()