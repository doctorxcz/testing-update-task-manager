
# TaskManagerUI.py - uživatelské rozhraní, ke kterému se připojuje TaskRepository pro práci s databází v main.py. Žádné SQL zde, jen input() a print().

class TaskManagerUI:
    """Vstup od uživatele a výpis výsledků. Žádné SQL zde."""

    def __init__(self, repo):
        self.repo = repo

    def _ziskat_neprazdny_vstup(self, prompt):
        while True:
            hodnota = input(prompt)
            if not hodnota:
                print("Vstup nemůže být prázdný.")
                continue
            return hodnota

    def _ziskat_platne_id(self, prompt):
        while True:
            id_raw = input(prompt)
            if not id_raw.isdigit():
                print("Neplatný vstup, zadejte číslo.")
                continue
            if not self.repo.ukol_existuje(int(id_raw)):
                print(f"Úkol s ID {id_raw} neexistuje, zkuste znovu.")
                continue
            return int(id_raw)

    def pridat_ukol(self):
        nazev = self._ziskat_neprazdny_vstup("Zadejte název úkolu: ")
        popis = self._ziskat_neprazdny_vstup("Zadejte popis úkolu: ")
        self.repo.pridat_ukol(nazev, popis)
        print(f"Úkol '{nazev}' byl přidán s výchozím stavem 'Nezahájeno'.")

    def zobrazit_ukoly(self):
        ukoly = self.repo.zobrazit_ukoly()
        if not ukoly:
            print("Seznam je prázdný – žádné aktivní úkoly.")
            return False
        print("\nSeznam úkolů:")
        for ukol in ukoly:
            print(f"{ukol[0]}. {ukol[1]} - {ukol[2]} | stav: {ukol[3]}")
        return True

    def aktualizovat_ukol(self):
        if not self.zobrazit_ukoly():
            return
        id_ukolu = self._ziskat_platne_id("Zadejte ID úkolu, který chcete aktualizovat: ")
        stavy = {"1": "probíhá", "2": "hotovo"}
        print("Nový stav: 1. Probíhá  2. Hotovo")
        while True:
            volba = input("Vyberte nový stav (1-2): ")
            if volba not in stavy:
                print("Neplatná volba, zkuste znovu.")
                continue
            break
        self.repo.aktualizovat_ukol(id_ukolu, stavy[volba])
        print(f"Stav úkolu č. {id_ukolu} byl aktualizován na '{stavy[volba]}'.")

    def odstranit_ukol(self):
        # Odstranění úkolu doplněné o kontrolu bezpečného smazání s potvrzením od uživatele, aby se předešlo nechtěnému smazání.
        if not self.zobrazit_ukoly():
            return
        id_ukolu = self._ziskat_platne_id("Zadejte ID úkolu, který chcete odstranit: ")
        potvrzeni = input(f"Opravdu chcete smazat úkol č. {id_ukolu}? (ano/ne): ")
        if potvrzeni.lower() != "ano":
            print("Mazání zrušeno.")
            return
        self.repo.odstranit_ukol(id_ukolu)
        print(f"Úkol č. {id_ukolu} byl trvale odstraněn z databáze.")

    def hlavni_menu(self):
        """ Hlavní menu pro interakci s uživatelem. Volby pro přidání, zobrazení, aktualizaci a odstranění úkolů, plus možnost ukončit program."""
        while True:
            print("\nSprávce úkolů - Hlavní menu")
            print("1. Přidat úkol")
            print("2. Zobrazit úkoly")
            print("3. Aktualizovat úkol")
            print("4. Odstranit úkol")
            print("5. Ukončit program")

            volba = input("Vyberte možnost (1-5): ")

            if volba == "1":
                self.pridat_ukol()
            elif volba == "2":
                self.zobrazit_ukoly()
            elif volba == "3":
                self.aktualizovat_ukol()
            elif volba == "4":
                self.odstranit_ukol()
            elif volba == "5":
                print("\nKonec programu.")
                break
            else:
                print("Neplatná volba, zkuste znovu.")
