import csv

def load_data(filename):
    kms = []
    prices = []
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kms.append(int(row["km"]))
                prices.append(int(row["price"]))
    except FileNotFoundError:
        print(f"Erreur : le fichier '{filename}' est introuvable.")
        exit(1)
    except ValueError:
        print("Erreur : le fichier contient une valeur non numérique.")
        exit(1)
    except Exception as e:
        print(f"Probleme avec le csv : {e}")
        exit(1)
    return kms, prices

def normalize(data):
    mini = min(data)
    maxi = max(data)
    if maxi == mini:
        norm = [0.0 for _ in data]
    norm = [(x - mini) / (maxi - mini) for x in data]
    return norm, mini, maxi

def train(kms, prices, learning_rate=0.1, iterations=10000):
    theta0 = 0.0
    theta1 = 0.0
    m = len(kms)

    for _ in range(iterations):
        tmp_θ0 = sum((theta0 + theta1 * kms[i]) - prices[i] for i in range(m))
        # 2. calculer la somme des erreurs × km pour tmp_θ1
        # 3. mettre à jour theta0 et theta1 simultanément

    return theta0, theta1

def main():
    kms, prices = load_data("data.csv")
    kms_norm, km_min, km_max = normalize(kms)
    prices_norm, price_min, price_max = normalize(prices)
    print(kms)
    print(kms_norm)

if __name__ == "__main__":
    main()