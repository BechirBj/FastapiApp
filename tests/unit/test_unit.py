from app.utils import is_valid_salary


def test_salary_is_valid():
    assert is_valid_salary(2500) is True


def test_salary_cannot_be_zero():
    assert is_valid_salary(0) is False


def test_salary_cannot_be_negative():
    assert is_valid_salary(-500) is False