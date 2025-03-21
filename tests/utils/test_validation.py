import pytest

from utils.validation import validate_menu_selection, validate_number_of_tickets, validate_string_input, validate_title_rows_seats_per_row


@pytest.mark.parametrize(
    "title_rows_seats_per_row_str, is_valid",
    [
        (None, (False, None, None, None)),
        ("", (False, None, None, None)),
        ("Abc 10", (False, None, None, None)),
        ("8 10", (False, None, None, None)),
        (" 8 10", (False, None, None, None)),
        ("Inception 8.8 10", (False, None, None, None)),
        ("Inception 8 10.5", (False, None, None, None)),
        ("Inception 0 10", (False, None, None, None)),
        ("Inception 8 0", (False, None, None, None)),
        ("Inception -1 10", (False, None, None, None)),
        ("Inception 8 -10", (False, None, None, None)),
        ("Inception 27 10", (False, None, None, None)),
        ("Inception 26 55", (False, None, None, None)),
        ("Inception 8 10", (True, "Inception", 8, 10)),
    ],
)
def test_validate_title_rows_seats_per_row(title_rows_seats_per_row_str, is_valid):
    result = validate_title_rows_seats_per_row(title_rows_seats_per_row_str)
    assert result == is_valid


@pytest.mark.parametrize(
    "selection_str, is_valid",
    [
        (None, (False, None)),
        ("", (False, None)),
        ("4", (False, None)),
        ("1", (True, "1")),
        ("2", (True, "2")),
        ("3", (True, "3")),
    ],
)
def test_validate_menu_selection(selection_str, is_valid):
    result = validate_menu_selection(selection_str)
    assert result == is_valid


@pytest.mark.parametrize(
    "number_of_tickets_str, is_valid",
    [
        (None, (False, None)),
        ("", (False, None)),
        ("0", (False, None)),
        ("-8", (False, None)),
        ("4", (True, 4)),
    ],
)
def test_validate_number_of_tickets(number_of_tickets_str, is_valid):
    result = validate_number_of_tickets(number_of_tickets_str)
    assert result == is_valid


@pytest.mark.parametrize(
    "input_str, is_valid",
    [
        (None, (False, None)),
        ("", (False, None)),
        ("   ", (False, None)),
        ("B03", (True, "B03")),
        ("GIC0004", (True, "GIC0004")),
    ],
)
def test_validate_string_input(input_str, is_valid):
    result = validate_string_input(input_str)
    assert result == is_valid
