text = ''' Fostul ministru Eduard Novak a postat miercuri pe Facebook un mesaj prin care acuză premierile
făcute după Jocurile Olimpice, el precizând că secretarul general al Federaţiei Române de Canotaj şi
contabilul şef al forului au primit premii mai mari decât campionul David Popovici. Preşedinta Agenţiei
Naţionale pentru Sport, Elisabeta Lipă, a reacţionat spunând că Novak ar trebui să consulte normele
financiare şi atunci ar vedea că nu s-a încălcat nicio lege '''

def articol(text):
    # Împărțirea șirului în două părți egale
    jumatate = len(text) // 2
    part1 = text[:jumatate]
    part2 = text[jumatate:]

    # Pe prima parte:
    part1 = part1.upper().strip()  # Transformă în majuscule și elimină spațiile goale

    # Pe a doua parte:
    part2 = part2[::-1]  # Inversează ordinea caracterelor
    part2 = part2.capitalize()  # Transformă prima literă în majusculă
    punctuatie = '.,!?'
    part2 = ''.join(char for char in part2 if char not in punctuatie)  # Elimină caracterele de punctuație

    # Combină cele două părți
    rezultat = part1 + ' ' + part2
    return rezultat

# Afișează rezultatul
rezultat = articol(text)
print(rezultat)