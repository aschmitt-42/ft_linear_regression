import csv
import json

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
        sum_errors = 0
        sum_errors_km = 0

        for i in range(m):
            sum_errors += (theta0 + theta1 * kms[i]) - prices[i] # sum_errors = sum((theta0 + theta1 * kms[i]) - prices[i] for i in range(m))
            sum_errors_km += ((theta0 + theta1 * kms[i]) - prices[i]) * kms[i] # sum_errors_km = sum(((theta0 + theta1 * kms[i]) - prices[i]) * kms[i] for i in range(m))
        theta0, theta1 = theta0 - learning_rate * (1/m) * sum_errors, theta1 - learning_rate * (1/m) * sum_errors_km

    return theta0, theta1

def denormalize_thetas(theta0, theta1, km_min, km_max, price_min, price_max):
    theta1_real = theta1 * (price_max - price_min) / (km_max - km_min)
    theta0_real = theta0 * (price_max - price_min) + price_min - theta1_real * km_min
    return theta0_real, theta1_real

def main():
    kms, prices = load_data("data.csv")
    kms_norm, km_min, km_max = normalize(kms)
    prices_norm, price_min, price_max = normalize(prices)

    theta0, theta1 = train(kms_norm, prices_norm)
    theta0, theta1 = denormalize_thetas(theta0, theta1, km_min, km_max, price_min, price_max)
    print(f"Entraînement terminé. theta0={theta0:.2f}, theta1={theta1:.2f}")

    try:
        with open("thetas.json", "w") as f:
            json.dump({"theta0": theta0, "theta1": theta1}, f)
    except Exception as e:
        print(f"Probleme avec le thetas.json : {e}")
        exit(1)


if __name__ == "__main__":
    main()