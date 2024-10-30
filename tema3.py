meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
istoric_comenzi = []

#Comanda
#Comanda

for i in range(len(studenti)):
    student = studenti.pop()
    comanda =  comenzi.pop()
    tavi.pop()
    istoric_comenzi.append(comanda)
    print(f"{student} a comandat {comanda}")

#Inventar

papanasi_inceput =  meniu.count("papanasi")
papanasi_comandat = istoric_comenzi.count("papanasi")
pret_papanasi = preturi[0][1]
print(f"S-au comandat {papanasi_comandat} portii de papanasi")

ceafa_inceput = meniu.count("ceafa")
ceafa_comandat = comenzi.count("ceafa")
pret_ceafa = preturi[1][1]
print(f"S-au comandat {ceafa_comandat} portii de ceafa")

guias_inceput = meniu.count("guias")
guias_comandat = comenzi.count("guias")
pret_guias = preturi[2][1]
print(f"S-au comandat {guias_comandat} portii de guias")

tavi_ramase = len(tavi)
print(f"Au ramas {tavi_ramase} tavi disponibile")

print("Mai sunt papanasi?", papanasi_inceput > papanasi_comandat)
print("Mai este ceafa?", ceafa_inceput > ceafa_comandat)
print("Mai este guias?" , guias_inceput > guias_comandat)

#Incasare

incasare = papanasi_comandat*pret_papanasi + ceafa_inceput*pret_ceafa + guias_inceput*pret_guias

print(f"Cantina a incasat: {incasare} lei")

print("\n")
print("Produse care costa cel mult 7 lei:")
for produs in preturi:
    if produs[1] <= max :
        print(produs)