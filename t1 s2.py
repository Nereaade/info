import random
import csv
import os

GENDER_CODES = {"M": [1, 5], "F": [2, 6]}

COUNTY = [str(i).zfill(2) for i in range(1, 40)] + ["51", "52"]

county_code = {
    "01": "Alba",
    "02": "Arad",
    "03": "Argeș",
    "04": "Bacău",
    "05": "Bihor",
    "06": "Bistrița-Năsăud",
    "07": "Botoșani",
    "08": "Brașov",
    "09": "Brăila",
    "10": "Buzău",
    "11": "Caraș-Severin",
    "12": "Cluj",
    "13": "Constanța",
    "14": "Covasna",
    "15": "Dâmbovița",
    "16": "Dolj",
    "17": "Galați",
    "18": "Gorj",
    "19": "Harghita",
    "20": "Hunedoara",
    "21": "Ialomița",
    "22": "Iași",
    "23": "Ilfov",
    "24": "Maramureș",
    "25": "Mehedinți",
    "26": "Mureș",
    "27": "Neamț",
    "28": "Olt",
    "29": "Prahova",
    "30": "Satu Mare",
    "31": "Sălaj",
    "32": "Sibiu",
    "33": "Suceava",
    "34": "Teleorman",
    "35": "Timiș",
    "36": "Tulcea",
    "37": "Vaslui",
    "38": "Vâlcea",
    "39": "Vrancea",
    "40": "București",
    "51": "Călărași",
    "52": "Giurgiu"
}

COUNTY_POPULATION_PERCENTAGE = {
    "01": 1.9, "02": 2.0, "03": 2.5, "04": 2.3, "05": 2.2, "06": 1.4,
    "07": 1.8, "08": 2.5, "09": 1.5, "10": 2.1, "11": 1.3, "12": 3.0,
    "13": 3.0, "14": 1.0, "15": 2.1, "16": 2.4, "17": 2.3, "18": 1.4,
    "19": 1.3, "20": 1.6, "21": 1.0, "22": 3.5, "23": 1.6, "24": 1.8,
    "25": 1.1, "26": 2.2, "27": 2.0, "28": 1.6, "29": 2.7, "30": 1.3,
    "31": 1.0, "32": 1.8, "33": 2.4, "34": 1.5, "35": 3.2, "36": 0.9,
    "37": 1.5, "38": 1.6, "39": 1.4, "40": 9.6, "51": 0.9, "52": 1.0
}

GENDER_DISTRIBUTION = {"M": 48.7, "F": 51.3}

AGE_GROUP_DISTRIBUTION = {
    "0-14": 15.7,
    "15-24": 9.6,
    "25-54": 45.6,
    "55-64": 13.5,
    "65+": 15.6
}

MALE_NAMES = ["Andrei", "Mihai", "Alexandru", "Stefan", "Daniel", "Lucas", "Emanuel", "Gigel", "Constantin", "Mitru",
              "Mirel", "Adrian", "Bogdan", "Eric", "Darius", "Cosmin", "Dragos", "Tomy", "Gavrila"]
FEMALE_NAMES = ["Maria", "Ioana", "Elena", "Gabriela", "Ana", "Mihaela", "Mara", "Florina", "Lenuta", "Paula", "Alexia",
                "Diana", "Daniela", "Carmen", "Laura", "Letita", "Alexandra", "Aura", "Irene"]
LAST_NAMES = ["Popescu", "Ionescu", "Dumitru", "Stan", "Gheorghe", "Gaie", "Pop", "Nicoara", "Mihut", "Covacs",
              "Muresan", "Moisza", "Boitor", "Moga", "Frandos", "Cosma"]


def select_weighted_choice(distribution_dict):
    choices = list(distribution_dict.keys())
    weights = list(distribution_dict.values())
    return random.choices(choices, weights=weights, k=1)[0]


def generate_cnp(gender: str) -> str:
    age_group = select_weighted_choice(AGE_GROUP_DISTRIBUTION)

    if age_group == "0-14":
        year = random.randint(2010, 2024)
    elif age_group == "15-24":
        year = random.randint(2000, 2009)
    elif age_group == "25-54":
        year = random.randint(1970, 1999)
    elif age_group == "55-64":
        year = random.randint(1960, 1969)
    else:
        year = random.randint(1920, 1959)

    month = random.randint(1, 12)
    day = random.randint(1, 28)
    county = select_weighted_choice(COUNTY_POPULATION_PERCENTAGE)
    order_number = random.randint(100, 999)

    if year < 2000:
        first_digit = 1 if gender == "M" else 2
    else:
        first_digit = 5 if gender == "M" else 6

    yy = str(year % 100).zfill(2)
    mm = str(month).zfill(2)
    dd = str(day).zfill(2)

    partial_cnp = f"{first_digit}{yy}{mm}{dd}{county}{order_number}"
    control_digit = random.randint(0, 9)
    return partial_cnp + str(control_digit)


def generate_csv(filename: str, num_entries: int = 1_000_000):
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CNP", "First Name", "Last Name"])

        for _ in range(num_entries):
            gender = select_weighted_choice(GENDER_DISTRIBUTION)
            first_name = random.choice(MALE_NAMES if gender == "M" else FEMALE_NAMES)
            last_name = random.choice(LAST_NAMES)
            cnp = generate_cnp(gender)
            writer.writerow([cnp, first_name, last_name])

    print(f"CSV file generated successfully at: {filepath}")

class HashTable:
    def __init__(self, size=100003):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash_function(self, cnp):
        return sum(ord(char) for char in cnp) % self.size

    def insert(self, cnp, first_name, last_name):
        index = self._hash_function(cnp)
        self.table[index].append((cnp, first_name, last_name))

    def search(self, cnp):
        index = self._hash_function(cnp)
        for record in self.table[index]:
            if record[0] == cnp:
                return record
        return None

    def search_with_iterations(self, cnp):
        index = self._hash_function(cnp)
        bucket = self.table[index]

        for i, record in enumerate(bucket):
            if record[0] == cnp:
                return record, i + 1

        return None, len(bucket)

database = HashTable()

csv_filename = "cnp_data.csv"
try:
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sare peste header
        all_cnp = []

        for row in reader:
            cnp, first_name, last_name = row
            database.insert(cnp, first_name, last_name)
            all_cnp.append(cnp)

except FileNotFoundError:
    print(f"Fișierul {csv_filename} nu a fost găsit. Asigură-te că ai generat CSV-ul corect.")

if all_cnp:
    selected_cnp = random.sample(all_cnp, 1000)
    total_iterations = 0
    county_count = {county: 0 for county in county_code.values()}

    for cnp in selected_cnp:
        _, iterations = database.search_with_iterations(cnp)
        total_iterations += iterations
        county_code_value = cnp[7:9]  # Extrage codul județului din CNP
        county_name = county_code.get(county_code_value, "Necunoscut")
        county_count[county_name] += 1

    avg_iterations = total_iterations / len(selected_cnp)
    print(f"Număr total de iterații: {total_iterations}")
    print(f"Număr mediu de iterații per căutare: {avg_iterations:.2f}")

    print("\nDistribuția pe județe pentru cele 1000 de CNP-uri căutate:")
    for county, count in sorted(county_count.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            percentage = (count / len(selected_cnp)) * 100
            print(f"{county}: {count} CNP-uri ({percentage:.2f}%)")
