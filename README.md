# Vylepšený Task Manager

## Popis
Správce úkolů s MySQL databází. CRUD operace + automatizované testy.

## Požadavky
- Python 3.x
- mysql-connector-python
- pytest

## Instalace
pip install mysql-connector-python pytest

## Spuštění
1. Vytvoř databázi v MySQL: CREATE DATABASE task_manager;
2. Spusť program: python main.py

## Testy
1. Vytvoř testovací databázi: CREATE DATABASE task_manager_test;
2. Spusť testy: pytest test_main.py
