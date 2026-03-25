import csv
import json
import matplotlib.pyplot as plt

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
        return [0.0 for _ in data], mini, maxi
    return [(x - mini) / (maxi - mini) for x in data], mini, maxi

def train(kms, prices, learning_rate=0.01, iterations=1000000):
    theta0 = 0.0
    theta1 = 0.0
    m = len(kms)
    snapshots = []
    checkpoints = {
        100,
        1000,
        2000,
        3000,
    }
    for n in range(iterations):
        sum_errors = 0
        sum_errors_km = 0
        for i in range(m):
            sum_errors += (theta0 + theta1 * kms[i]) - prices[i]
            sum_errors_km += ((theta0 + theta1 * kms[i]) - prices[i]) * kms[i]
        theta0, theta1 = theta0 - learning_rate * (1/m) * sum_errors, theta1 - learning_rate * (1/m) * sum_errors_km
        if n in checkpoints:
            snapshots.append((n + 1, theta0, theta1))
    return theta0, theta1, snapshots

def denormalize_thetas(theta0, theta1, km_min, km_max, price_min, price_max):
    theta1_real = theta1 * (price_max - price_min) / (km_max - km_min)
    theta0_real = theta0 * (price_max - price_min) + price_min - theta1_real * km_min
    return theta0_real, theta1_real

################################################ BONUS ################################################

def graphique(kms, prices, km_min, km_max, theta0, theta1, graphique):
    # plt.clear()
    plt.title("Prix d'une voiture en fonction du kilométrage")
    plt.xlabel("Kilométrage (km)")
    plt.ylabel("Prix (euros)")

    # Points
    plt.scatter(kms, prices, color="#D4956A")

    # Droite
    x = [km_min, km_max]
    y = [theta0 + theta1 * km_min, theta0 + theta1 * km_max]
    plt.plot(x, y, color="#4A90D9") 

    # Erreur
    for i in range(len(kms)):
        estimation = theta0 + theta1 * kms[i]
        plt.plot([kms[i], kms[i]], [prices[i], estimation], color="red", linestyle="dashed", linewidth=0.8, alpha=0.6)

    # plt.show()
    plt.savefig(graphique)

def graphique_evolution(kms, prices, km_min, km_max, price_min, price_max, snapshots):
    for n_iter, t0_norm, t1_norm in snapshots:
        t0, t1 = denormalize_thetas(t0_norm, t1_norm, km_min, km_max, price_min, price_max)
        plt.figure()
        plt.title(f"Itération {n_iter}")
        plt.xlabel("Kilométrage (km)")
        plt.ylabel("Prix (euros)")
        plt.scatter(kms, prices, color="#D4956A")
        x = [km_min, km_max]
        y = [t0 + t1 * km_min, t0 + t1 * km_max]
        plt.plot(x, y, color="#4A90D9")
        for i in range(len(kms)):
            estimation = t0 + t1 * kms[i]
            plt.plot([kms[i], kms[i]], [prices[i], estimation],
                     color="#E8603C", linestyle="dashed", linewidth=0.8, alpha=0.6)
        plt.savefig(f"graphique_iter_{n_iter}.png")
        plt.close()


# quelle proportion de la variation des prix mon modèle explique-t-il ? 
# est-ce que la variable X (km) permet de prédire la variable Y (prix)
def r2_score(kms, prices, theta0, theta1): 
    res = 0
    total = 0
    mean_price = sum(prices) / len(prices)
    for i in range(len(prices)):
        res += (prices[i] - (theta0 + theta1 * kms[i])) **2  # erreurs du modèle
        total += (prices[i] - mean_price) **2                # erreurs par rapport à la moyenne
    r2 = 1 - (res / total)
    print(f"Précision du modèle (R²) : {r2:.4f}")


#######################################################################################################

def main():
    kms, prices = load_data("data.csv")
    kms_norm, km_min, km_max = normalize(kms)
    prices_norm, price_min, price_max = normalize(prices)

    theta0, theta1, snapshots = train(kms_norm, prices_norm)
    theta0, theta1 = denormalize_thetas(theta0, theta1, km_min, km_max, price_min, price_max)
    print(f"Entraînement terminé. theta0={theta0:.2f}, theta1={theta1:.2f}")
    try:
        with open("thetas.json", "w") as f:
            json.dump({"theta0": theta0, "theta1": theta1}, f)
    except Exception as e:
        print(f"Probleme avec le thetas.json : {e}")
        exit(1)
    graphique(kms, prices, km_min, km_max, theta0, theta1, "graphique_final.png")
    graphique_evolution(kms, prices, km_min, km_max, price_min, price_max, snapshots)
    r2_score(kms, prices, theta0, theta1)

if __name__ == "__main__":
    main()