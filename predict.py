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
        try:
            user_input = input("Entrez un kilométrage (ou 'q' pour quitter) : ")
            if user_input.lower() == "q":
                break

            kms = int(user_input)
            estimation = theta0 + theta1 * kms
            if (estimation < 0):
                estimation = 0
            print(f"Estimation du prix : {estimation:.0f} euros")
            
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue
        except KeyboardInterrupt:
            print("\nProgramme interrompu par l'utilisateur.")
            break

if __name__ == "__main__":
    main()