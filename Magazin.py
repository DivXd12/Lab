import json
import random

def calculate_change(change, denominations, stock):
    """Calculates the optimal change using dynamic programming."""

    denominations.sort(reverse=True)  # Sort denominations in descending order
    n = len(denominations)
    dp = [float('inf')] * (change + 1)
    dp[0] = 0
    count = [([0] * n) for _ in range(change + 1)]


    for i in range(1, change + 1):
        for j in range(n):
            val = denominations[j]
            if i - val >= 0 and dp[i - val] + 1 < dp[i] and stock[j] > count[i-val][j]:
                dp[i] = dp[i - val] + 1
                count[i] = count[i-val][:]
                count[i][j] +=1

    if dp[change] == float('inf'):
        return None  # No solution found

    change_result = {}
    for i in range(n):
        if count[change][i]>0:
            change_result[denominations[i]] = count[change][i]

    return change_result


def simulate_cash_register(filepath="cash_register_data.json"):
    """Simulates the cash register operation."""

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")
        return


    denominations = [bill["valoare"] for bill in data["bancnote"]]
    stock = [bill["stoc"] for bill in data["bancnote"]]
    products = data["produse"]

    while True:
        product = random.choice(products)
        payment = product["pret"] + random.randint(1, 20)
        change = payment - product["pret"]

        change_result = calculate_change(change, denominations, stock)


        if change_result is None:
            print("\nCannot give change! Simulation stopped.")
            print(f"  Product: {product['nume']}, Price: {product['pret']}, Payment: {payment}")
            print("  Available banknotes:", data['bancnote'])
            return

        print(f"\nProduct: {product['nume']}, Price: {product['pret']}, Payment: {payment}")
        print(f"Change: {change}")
        print("Banknotes used:", change_result)



        for i, val in enumerate(denominations):
            stock[i] -= change_result.get(val,0)

        #print ("Stoc:",stock)


# Create sample JSON data if file doesn't exist.

try:
    with open("cash_register_data.json", "x") as f:
        json.dump({
            "bancnote": [
                {"valoare": 50, "stoc": 20},
                {"valoare": 20, "stoc": 30},
                {"valoare": 10, "stoc": 40},
                {"valoare": 5, "stoc": 50},
                {"valoare": 1, "stoc": 100}
            ],
            "produse": [
                {"nume": "Lapte", "pret": 7},
                {"nume": "Paine", "pret": 3},
                {"nume": "Ciocolata", "pret": 5},
                {"nume": "Apa", "pret": 2},
                {"nume": "Cafea", "pret": 9}
            ]
        }, f, indent=2)

except FileExistsError:
    pass  # File already exists


simulate_cash_register()