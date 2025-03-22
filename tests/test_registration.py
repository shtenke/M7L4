import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test1(setup_database):
    username = 'shtenke'
    test = add_user(username,'shtenke@mail.ru','34564357')
    assert test == False
    
def test2(setup_database):
    username = 'shtenke'
    password = 'etrhteh'
    authenticate_user(username,password)
    assert 'Авторизация успешна.'

def test3(setup_database):
    username = 'shtenke2'
    password = 'etrhteh'
    authenticate_user(username,password)
    assert 'Неверный логин или пароль.'

def test4(setup_database):
    username = 'shtenke'
    password = 'etrhtehrethrytukyuk'
    authenticate_user(username,password)
    assert 'Неверный логин или пароль.'

def test5(setup_database,capsys):
    display_users()
    captured = capsys.readouterr()
    assert "Логин: shtenke, Электронная почта: w4gergh" in captured.out
# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""