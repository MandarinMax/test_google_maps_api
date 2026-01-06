import pytest
import os


@pytest.fixture
def temp_file():
    # --- SETUP ---
    file_path = "temp_test_file.txt"
    with open(file_path, "w") as f:
        f.write("hello pytest")

    yield file_path

    # --- TEARDOWN ---
    print(f"\nУдаление файла {file_path}")
    os.remove(file_path)


def test_read_from_temp_file(temp_file):
    with open(temp_file, "r") as f:
        content = f.read()
    assert content == "hello pytest"
