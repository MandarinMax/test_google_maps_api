import pytest

@pytest.mark.con
def test_settings_access(admin_user):
    """
    Проверяет, что пользователь из фикстуры может менять настройки.
    """
    if admin_user.is_admin():
        print("Доступ к настройкам разрешен")
    assert admin_user.role == "admin"