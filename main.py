# importy a načítání .env
import os
from dotenv import load_dotenv
from TaskManagerUI import TaskManagerUI
from database_connect import pripojeni_db

load_dotenv()


class TaskRepository:
    """Veškerá komunikace s MySQL databází. Žádný input() zde."""

    def __init__(self, conn):
        self.conn = conn

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
            ''')
            cursor.execute("SHOW TABLES LIKE 'ukoly'")
            if cursor.fetchone():
                print("Tabulka 'ukoly' byla úspěšně vytvořena a ověřena v databázi.")
            else:
                print("Chyba: tabulka 'ukoly' nebyla vytvořena.")
        cursor.close()

    def pridat_ukol(self, nazev, popis):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)
        ''', (nazev, popis, 'nezahájeno'))
        # commit je nutný – bez něj INSERT nebude zapsán na disk
        self.conn.commit()
        cursor.close()

    def zobrazit_ukoly(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, nazev, popis, stav FROM ukoly
        WHERE stav IN ('nezahájeno', 'probíhá')
        ''')
        ukoly = cursor.fetchall()
        cursor.close()
        return ukoly

    def ukol_existuje(self, id_ukolu):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM ukoly WHERE id = %s', (id_ukolu,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def aktualizovat_ukol(self, id_ukolu, stav):
        if not self.ukol_existuje(id_ukolu):
            return False
        cursor = self.conn.cursor()
        cursor.execute('UPDATE ukoly SET stav = %s WHERE id = %s', (stav, id_ukolu))
        self.conn.commit()
        cursor.close()
        return True

    def odstranit_ukol(self, id_ukolu):
        if not self.ukol_existuje(id_ukolu):
            return False
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM ukoly WHERE id = %s', (id_ukolu,))
        self.conn.commit()
        cursor.close()
        return True


# --- hlavní program ---
if __name__ == "__main__":
    conn = pripojeni_db(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    if conn:
        repo = TaskRepository(conn)
        repo.vytvoreni_tabulky()
        ui = TaskManagerUI(repo)
        ui.hlavni_menu()
        conn.close()
