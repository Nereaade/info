import random
import json
data = {
    "bancnote": [
        { "valoare": 50, "stoc": 20 },
        { "valoare": 20, "stoc": 30 },
        { "valoare": 10, "stoc": 40 },
        { "valoare": 5, "stoc": 50 },
        { "valoare": 1, "stoc": 100 }
    ],
    "produse": [
        { "nume": "Lapte", "pret": 7 },
        { "nume": "Paine", "pret": 3 },
        { "nume": "Ciocolata", "pret": 5 },
        { "nume": "Apa", "pret": 2 },
        { "nume": "Cafea", "pret": 9 }
    ]
}

def calculeaza_rest(rest, bancnote):
    dp = [float('inf')] * (rest + 1)
    dp[0] = 0
    combinatii = [{} for _ in range(rest + 1)]

    for bancnota in bancnote:
        val = bancnota["valoare"]
        stoc = bancnota["stoc"]
        for r in range(rest, -1, -1):
            for k in range(1, stoc + 1):
                if r - k * val >= 0 and dp[r - k * val] + k < dp[r]:
                    dp[r] = dp[r - k * val] + k
                    combinatii[r] = combinatii[r - k * val].copy()
                    combinatii[r][val] = combinatii[r].get(val, 0) + k

    return None if dp[rest] == float('inf') else combinatii[rest]

def actualizeaza_stoc(stoc, rest_obtinut):
    for val, cant in rest_obtinut.items():
        for b in stoc:
            if b["valoare"] == val:
                b["stoc"] -= cant

def simuleaza_clienti(data):
    produse = data["produse"]
    bancnote = data["bancnote"]
    client_id = 1

    while True:
        nr_produse = random.randint(1, 5)
        cos = random.choices(produse, k=nr_produse)

        total = sum(p["pret"] for p in cos)
        suma_platita = total + random.randint(1, min(20, 100 - total))
        rest = suma_platita - total

        rest_obtinut = calculeaza_rest(rest, bancnote)

        print(f"\n Client #{client_id}")
        print(" - Produse cumpărate:")
        for p in cos:
            print(f"   • {p['nume']} - {p['pret']} RON")
        print(f" - Total de plată: {total} RON")
        print(f" - Suma plătită: {suma_platita} RON")
        print(f" - Rest de oferit: {rest} RON")

        if rest_obtinut is None:
            print("\n Nu se poate oferi restul cu bancnotele disponibile.")
            print("Stoc bancnote actual:")
            for b in bancnote:
                print(f" - {b['valoare']} RON: {b['stoc']} buc")
            break

        print("Rest oferit:")
        for val in sorted(rest_obtinut, reverse=True):
            print(f" - {rest_obtinut[val]} x {val} RON")

        actualizeaza_stoc(bancnote, rest_obtinut)
        client_id += 1

if __name__ == "__main__":
    simuleaza_clienti(data)
