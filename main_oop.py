import json
import csv
import os


class Bilet:
    def __init__(self, znizka, typ, nazwa, cena):
        self.znizka = znizka
        self.typ = typ
        self.nazwa = nazwa
        self.cena = float(cena)


class Koszyk:
    def __init__(self):
        self.pozycje = []

    def dodaj(self, bilet, ilosc):
        self.pozycje.append((bilet, ilosc))

    def pokaz(self):
        if not self.pozycje:
            print("Koszyk pusty")
            return 0.0

        total = 0.0

        print("\nKOSZYK:")

        for bilet, ilosc in self.pozycje:
            suma = bilet.cena * ilosc
            total += suma

            print(
                f"{bilet.nazwa} "
                f"({bilet.znizka}, {bilet.typ}) "
                f"x{ilosc} = {suma:.2f}"
            )

        print(f"Razem: {total:.2f}")

        return total

    def wyczysc(self):
        self.pozycje.clear()


class AutomatBiletowy:
    def __init__(self):
        self.bilety = []
        self.koszyk = Koszyk()

    def wczytaj_ceny(self, fname):
        if fname.endswith(".json"):
            with open(fname, encoding="utf-8") as f:
                data = json.load(f)

            for znizka, typy in data.items():
                for typ, items in typy.items():
                    for nazwa, cena in items.items():
                        self.bilety.append(
                            Bilet(
                                znizka,
                                typ,
                                nazwa,
                                cena
                            )
                        )

        else:
            with open(
                fname,
                "r",
                encoding="utf-8-sig"
            ) as f:

                for row in csv.DictReader(f, delimiter=";"):
                    cena = float(
                        row["price"].replace(",", ".")
                    )

                    self.bilety.append(
                        Bilet(
                            row["discount"],
                            row["duration"],
                            row["name"],
                            cena
                        )
                    )

    def dodaj_bilet(self):
        znizka = input(
            "[N]ormalny / [U]lgowy: "
        ).lower()

        if znizka not in ("n", "u"):
            print("Zły wybór")
            return

        znizka = (
            "normalny"
            if znizka == "n"
            else "ulgowy"
        )

        typ = input(
            "[O]kresowy / [C]zasowy / [J]ednorazowy: "
        ).lower()

        typ_map = {
            "o": "okresowy",
            "c": "czasowy",
            "j": "jednorazowy"
        }

        if typ not in typ_map:
            print("Zły wybór")
            return

        typ = typ_map[typ]

        dostepne = [
            bilet
            for bilet in self.bilety
            if bilet.znizka == znizka
            and bilet.typ == typ
        ]

        if not dostepne:
            print("Brak biletów")
            return

        print("Dostępne:")

        for i, bilet in enumerate(dostepne):
            print(
                f"[{i + 1}] "
                f"{bilet.nazwa} - "
                f"{bilet.cena:.2f}"
            )

        wybor = input("Wybierz: ")

        try:
            indeks = int(wybor) - 1
            bilet = dostepne[indeks]
        except (ValueError, IndexError):
            print("Zły wybór")
            return

        ilosc = input("Ilość (1-9): ").strip()

        if not ilosc.isdigit():
            print("Nieprawidłowa ilość")
            return

        ilosc = int(ilosc)

        if not 1 <= ilosc <= 9:
            print("Nieprawidłowa ilość")
            return

        self.koszyk.dodaj(bilet, ilosc)

        print(
            f"Dodano {ilosc} x {bilet.nazwa}"
        )

    def kasa(self):
        total = self.koszyk.pokaz()

        if total == 0:
            return

        while True:
            try:
                paid = float(
                    input("Wpłata (zł): ")
                    .replace(",", ".")
                )

                if paid < total:
                    print(
                        f"Brakuje "
                        f"{total - paid:.2f}"
                    )
                    continue

                print(
                    f"Reszta: "
                    f"{paid - total:.2f}"
                )

                print("Wydano bilety:")

                for bilet, ilosc in self.koszyk.pozycje:
                    print(
                        f"- {ilosc} x "
                        f"{bilet.nazwa}"
                    )

                self.koszyk.wyczysc()

                break

            except ValueError:
                print("Błędna kwota")

    def uruchom(self):
        print("=== AUTOMAT BILETOWY ===")

        while True:
            cmd = input(
                "\n[D]odaj  [K]asa  [W]yjście: "
            ).lower()

            if cmd == "d":
                self.dodaj_bilet()

            elif cmd == "k":
                self.kasa()

            elif cmd == "w":
                break

            else:
                print("Nieznane polecenie")

        print("Do widzenia")



BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

json_file = os.path.join(
    BASE_DIR,
    "prices.json"
)

csv_file = os.path.join(
    BASE_DIR,
    "prices.csv"
)

automat = AutomatBiletowy()

if os.path.exists(json_file):
    automat.wczytaj_ceny(json_file)

elif os.path.exists(csv_file):
    automat.wczytaj_ceny(csv_file)

else:
    print(
        "Nie znaleziono pliku "
        "prices.json ani prices.csv"
    )
    exit()

automat.uruchom()