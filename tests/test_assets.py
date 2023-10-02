import pytest

from asset_nums.assets import handle_id, check_progged


def test_handle_id_with_valid_id():
    # Valid ID '1111', expecting True
    result = handle_id('1111', check_progged)
    assert result is True


#
def test_handle_id_with_invalid_id():
    # Invalid ID '2222', expecting False
    result = handle_id('2222', check_progged)
    assert result is False


def test_handle_id_with_invalid_input():
    # Invalid input type, expecting TypeError
    with pytest.raises(ValueError):
        handle_id(1234, check_progged)


def test_handle_id_with_invalid_type():
    # Invalid input type, expecting TypeError
    with pytest.raises(TypeError):
        handle_id(dict(), check_progged)

