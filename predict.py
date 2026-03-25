import json

def load_thetas():
    try:
        with open("thetas.json", "r") as f:
            data = json.load(f)
        return data["theta0"], data["theta1"]
    except FileNotFoundError:
        return 0, 0


def main():
    theta0, theta1 = load_thetas()
    print(f"Initial theta0: {theta0}, Initial theta1: {theta1}\n")

    while True:
        user_input = input("Entrez un kilométrage (ou 'q' pour quitter) : ")

        if user_input.lower() == "q":
            break

        try:
            kms = int(user_input)
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        estimation = theta0 + theta1 * kms
        if (estimation < 0):
            estimation = 0
        print(f"Estimation du prix : {estimation:.0f} euros")

if __name__ == "__main__":
    main()