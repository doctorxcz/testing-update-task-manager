# Task Manager - Upgrade

Konzolová aplikace pro správu úkolů s MySQL databází.
Upgrade projektu od Engeto - oddělení datové vrstvy (TaskRepository)
od UI vrstvy (TaskManagerUI), unit testy přes pytest.

## Požadavky
- Python 3.10+
- MySQL server (lokálně nebo vzdáleně)

## Instalace

1. Naklonuj repozitář:
   mkdir task-manager-engeto
   cd task-manager-engeto
   git clone https://github.com/doctorxcz/testing-update-task-manager
   

3. Vytvoř a aktivuj virtuální prostředí:
   python3 -m venv venv
   source venv/bin/activate    # Mac/Linux
   venv\Scripts\activate       # Windows

4. Nainstaluj závislosti:
   pip install -r requirements.txt

5. Vytvoř soubor .env podle .env.example a vyplň přihlašovací údaje k MySQL.

## Spuštění
python main.py

## Testy
pytest -v

## Struktura projektu
- main.py - vstupní bod, TaskRepository (SQL vrstva)
- TaskManagerUI.py - uživatelské rozhraní (input/print)
- database_connect.py - připojení k MySQL
- test_main.py - unit testy pro TaskRepository
