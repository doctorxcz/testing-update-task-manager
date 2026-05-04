# Vylepšený Task Manager

## Popis
Vylepšený správce úkolů, který ukládá seznam do MySQL databáze provádí CREATE, READ, UPDATE, DELETE;
následuje pytest, který provede automatické testování hlavní nebo testovací dababáze s jedním pozitivním a jedním negativním výsledkem.

## Požadavky
- Python 3.x
- mysql-connector-python
- pytest

## Instalace
pip install mysql-connector-python pytest

## Spuštění
1. Vytvoř databázi v MySQL: CREATE DATABASE task_manager;
2. Spusť program: python3 main.py

## Testy
1. Vytvoř testovací databázi: CREATE DATABASE task_manager_test;
2. Spusť testy: pytest test_main.py
