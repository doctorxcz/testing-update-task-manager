""" test_main.py - testy pro TaskRepository, s připojením k testovací databázi, s nastavením a čištěním tabulky
    před a po každém testu, s ověřením funkcí pro přidání, aktualizaci a odstranění úkolů"""
import pytest
import mysql.connector
from main import TaskRepository # import TaskRepository z main.py pro testování funkcí přidání, aktualizace a odstranění úkolů


# připojení k testovací databázi s ověřením připojení, s nastavením parametrů pro testovací DB
@pytest.fixture(scope="module")
def db_conn():
    conn = mysql.connector.connect(
        host='localhost',
        database='task_manager_test',
        user='root',
        password=''
    )
    yield conn
    conn.close()


# vytvoření tabulky před každým testem, smazání dat po každém testu
@pytest.fixture(autouse=True)
def setup_tabulka(db_conn):
    cursor = db_conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(255) NOT NULL,
        popis TEXT,
        stav VARCHAR(50) NOT NULL DEFAULT 'nezahájeno' CHECK(stav IN ('nezahájeno', 'probíhá', 'hotovo')),
        datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    db_conn.commit()
    yield
    cursor.execute('DELETE FROM ukoly')
    db_conn.commit()
    cursor.close()


# instance TaskRepository s testovací DB
@pytest.fixture
def repo(db_conn):
    return TaskRepository(db_conn)


# --- pridat_ukol ---

def test_pridat_ukol_pozitivni(repo, db_conn):
    repo.pridat_ukol('Test úkol', 'Test popis')

    cursor = db_conn.cursor()
    cursor.execute("SELECT nazev, stav FROM ukoly WHERE nazev = 'Test úkol'")
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == 'Test úkol'
    assert result[1] == 'nezahájeno'


def test_pridat_ukol_negativni_nazev_none(repo):
    with pytest.raises(Exception):
        repo.pridat_ukol(None, 'Test popis')


# --- aktualizovat_ukol ---

def test_aktualizovat_ukol_pozitivni(repo, db_conn):
    repo.pridat_ukol('Aktualizační úkol', 'Popis')

    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Aktualizační úkol'")
    id_ukolu = cursor.fetchone()[0]
    cursor.close()

    result = repo.aktualizovat_ukol(id_ukolu, 'probíhá')

    cursor = db_conn.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    stav = cursor.fetchone()[0]
    cursor.close()

    assert result is True
    assert stav == 'probíhá'


def test_aktualizovat_ukol_negativni_neexistujici_id(repo):
    result = repo.aktualizovat_ukol(99999, 'hotovo')
    assert result is False


# --- odstranit_ukol ---

def test_odstranit_ukol_pozitivni(repo, db_conn):
    repo.pridat_ukol('Mazací úkol', 'Popis')

    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Mazací úkol'")
    id_ukolu = cursor.fetchone()[0]
    cursor.close()

    result = repo.odstranit_ukol(id_ukolu)

    cursor = db_conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
    zaznam = cursor.fetchone()
    cursor.close()

    assert result is True
    assert zaznam is None


def test_odstranit_ukol_negativni_neexistujici_id(repo):
    result = repo.odstranit_ukol(99999)
    assert result is False



