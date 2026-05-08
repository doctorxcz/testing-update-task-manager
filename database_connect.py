import mysql.connector
from mysql.connector import Error


def pripojeni_db(host, user, password, database, test=False):
    """Připojí se k MySQL databázi, vytvoří ji pokud neexistuje, a vrátí připojení
    pokud se připojení nezdaří, vrátí None. Parametr 'test' slouží k testovacím účelům a ovlivňuje chybové hlášení.
    
    """
    label = "testovací MySQL databázi" if test else "MySQL databázi"
    try:
        conn_init = mysql.connector.connect(host=host, user=user, password=password)
        cursor = conn_init.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.close()
        conn_init.close()
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        print(f"Připojení k {label} bylo úspěšné.")
        return conn
    except Error as e: # zachytí jakoukoliv chybu z mysql.connector a vypíše ji, včetně chyb připojení, autentizace, atd.
        print(f"Chyba při připojení k {label}: {e}")
        return None