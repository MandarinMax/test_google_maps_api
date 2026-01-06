
def test_file_creation_and_reading(tmp_path):
    print(f"Временная папка: {tmp_path}")
    #Создаем директорию внутри временной папки
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    file_patch = data_dir / "my_file.txt"
    # Создаем путь к нашему файлу
    file_path = data_dir / "my_file.txt"

    # Записываем в файл текст с помощью удобного метода
    file_path.write_text("Hello from tmp_path!")

    assert file_path.exists()
    assert file_path.read_text() == "Hello from tmp_path!"


def greet(name):
    print(f"Hello, {name}!")

def test_greet_prints_correct_output(capsys):
    # 1. Запрашиваем фикстуру

    # 2. Вызываем функцию, которая печатает в консоль
    greet("World")

    # 3. "Читаем" всё, что было захвачено
    captured = capsys.readouterr()

    # 4. Проверяем, что захваченный stdout соответствует ожиданиям
    assert captured.out == "Hello, World!\n"

def test_another_greet(capsys):
    greet("Alice")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"
    # Проверяем, что в stderr ничего не попало
    assert captured.err == ""
