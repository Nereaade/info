import random

cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]  # afisez ca str, si litere incercate+= lierea.isalpha()

# 2. Inițializarea numărului de încercări
incercari_ramase = 6
litere_incercate = []

print(progres)
ghicit = False

while not ghicit and incercari_ramase > 0:
    litera_introdusa = input("Type a letter ")
    if len(litera_introdusa) != 1 or not litera_introdusa.isalpha():
        print("Error! Please type a letter.")
        continue
    litere_incercate.append(litera_introdusa)
    de_afisat = " ".join(progres)
    print(de_afisat)
    if incercari_ramase == 0:
        print("No more tries left, try again")
    if litera_introdusa in cuvant_de_ghicit:
        for i in range(len(cuvant_de_ghicit)):
            if cuvant_de_ghicit[i] == litera_introdusa:
                progres[i] = litera_introdusa
        print(progres)
    else:
        incercari_ramase -= 1
        print(f"There are {incercari_ramase} tries left")

    if "_" not in progres:
        ghicit = True

if ghicit :
    print(f"Congratulations! You guessed the cord {cuvant_de_ghicit}")
else :
    print(f"You lost... The word was {cuvant_de_ghicit}")
