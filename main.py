# import python databázového modulu
import mysql.connector
from mysql.connector import Error

# funkce pro připojení k MySQL databázi, bez uživatelského vstupu
def pripojeni_db(host, database, user, password):
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("Připojení k MySQL databázi bylo úspěšné.")
        return conn
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

# třída pro komunikaci s databází, bez uživatelského vstupu
class TaskRepository:
    """Veškerá komunikace s MySQL databází. Žádný input() zde."""

    def __init__(self, conn):
        self.conn = conn
    # metoda pro vytvoření tabulky, pokud neexistuje, s kontrolou existence a ověřením vytvoření
    def vytvoreni_tabulky(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'ukoly'")

        if cursor.fetchone():
            print("Tabulka 'ukoly' existuje.")
        else:
            cursor.execute('''
            CREATE TABLE ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT,
                stav VARCHAR(50) NOT NULL DEFAULT 'nezahájeno' CHECK(stav IN ('nezahájeno', 'probíhá', 'hotovo')),
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''') # vytvoření tabulky sql bez kontroly vstupů, s ověřením vytvoření
            cursor.execute("SHOW TABLES LIKE 'ukoly'")
            if cursor.fetchone():
                print("Tabulka 'ukoly' byla úspěšně vytvořena a ověřena v databázi.")
            else:
                print("Chyba: tabulka 'ukoly' nebyla vytvořena.")
        cursor.close()
    # metoda pro přidání úkolu, bez kontroly vstupů, s ověřením vložení
    def pridat_ukol(self, nazev, popis):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)
        ''', (nazev, popis, 'nezahájeno'))
        self.conn.commit()
        cursor.close()
    # metoda pro zobrazení úkolů, bez kontroly vstupů, s ověřením načtení
    def zobrazit_ukoly(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, nazev, popis, stav FROM ukoly
        WHERE stav IN ('nezahájeno', 'probíhá')
        ''')
        ukoly = cursor.fetchall()
        cursor.close()
        return ukoly
    # metoda pro kontrolu existence úkolu, bez kontroly vstupů s ověřením existence
    def ukol_existuje(self, id_ukolu):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM ukoly WHERE id = %s', (id_ukolu,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    # metoda pro aktualizaci úkolu, bez kontroly vstupů, s ověřením aktualizace
    def aktualizovat_ukol(self, id_ukolu, stav):
        if not self.ukol_existuje(id_ukolu):
            return False
        cursor = self.conn.cursor()
        cursor.execute('UPDATE ukoly SET stav = %s WHERE id = %s', (stav, id_ukolu))
        self.conn.commit()
        cursor.close()
        return True
    # metoda pro odstranění úkolu, bez kontroly vstupů, s ověřením odstranění
    def odstranit_ukol(self, id_ukolu):
        if not self.ukol_existuje(id_ukolu):
            return False
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM ukoly WHERE id = %s', (id_ukolu,))
        self.conn.commit()
        cursor.close()
        return True

# třída pro uživatelské rozhraní, bez SQL dotazů a komunikace s databází
class TaskManagerUI:
    """Vstup od uživatele a výpis výsledků. Žádné SQL zde."""
    # konstruktor přijímá instanci TaskRepository pro komunikaci s databází
    def __init__(self, repo):
        self.repo = repo
    # metoda pro získání ne-prázdného vstupu od uživatele, s kontrolou prázdného vstupu
    def _ziskat_neprazdny_vstup(self, prompt):
        while True:
            hodnota = input(prompt)
            if not hodnota:
                print("Vstup nemůže být prázdný.")
                continue
            return hodnota
    # metoda pro získání platného ID úkolu od uživatele, s kontrolou nečíselného vstupu a neexistujícího ID
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
    # metoda pro přidání úkolu, bez kontroly vstupů, s ověřením přidání
    def pridat_ukol(self):
        nazev = self._ziskat_neprazdny_vstup("Zadejte název úkolu: ")
        popis = self._ziskat_neprazdny_vstup("Zadejte popis úkolu: ")
        self.repo.pridat_ukol(nazev, popis)
        print(f"Úkol '{nazev}' byl přidán s výchozím stavem 'Nezahájeno'.")
    # metoda pro zobrazení úkolů, bez kontroly vstupů, s ověřením zobrazení
    def zobrazit_ukoly(self):
        ukoly = self.repo.zobrazit_ukoly()
        if not ukoly:
            print("Seznam je prázdný – žádné aktivní úkoly.")
            return False
        print("\nSeznam úkolů:")
        for ukol in ukoly:
            print(f"{ukol[0]}. {ukol[1]} - {ukol[2]} | stav: {ukol[3]}")
        return True
    # metoda pro aktualizaci úkolu, bez kontroly vstupů, s ověřením aktualizace
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
    # metoda pro odstranění úkolu, bez kontroly vstupů, s ověřením odstranění
    def odstranit_ukol(self):
        if not self.zobrazit_ukoly():
            return
        id_ukolu = self._ziskat_platne_id("Zadejte ID úkolu, který chcete odstranit: ")
        # potvrzení odstranění úkolu, dvojité ověření.
        potvrzeni = input(f"Opravdu chcete smazat úkol č. {id_ukolu}? (ano/ne): ")
        if potvrzeni.lower() != "ano":
            print("Mazání zrušeno.")
            return
        self.repo.odstranit_ukol(id_ukolu)
        print(f"Úkol č. {id_ukolu} byl trvale odstraněn z databáze.")
    # metoda pro hlavní menu, bez kontroly vstupů, s ověřením volby
    def hlavni_menu(self):
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

# hlavní část programu, bez kontroly vstupů, s ověřením připojení a spuštění UI
if __name__ == "__main__":
    conn = pripojeni_db(
        host='localhost',
        database='task_manager',
        user='root',
        password=''
    )
    # pokud je připojení úspěšné, vytvoří se instance TaskRepository, ověří se existence tabulky a spustí se UI
    if conn:
        repo = TaskRepository(conn)
        repo.vytvoreni_tabulky()
        ui = TaskManagerUI(repo)
        ui.hlavni_menu()
        conn.close()








