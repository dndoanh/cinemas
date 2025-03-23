import utils.constants as consts


def validate_title_rows_seats_per_row(title_rows_seats_per_row_str: str) -> tuple:
    """Validate string input of movie title, rows, seats per row.
    Args:
        title_rows_seats_per_row_str(str): input string of movie title, rows, seats per row.
    Return:
        a tuple values to indicate whether movie title, rows, seats per row are valid or not.
    """
    if not title_rows_seats_per_row_str:
        return False, None, None, None
    title_rows_seats_per_row = title_rows_seats_per_row_str.split()
    if len(title_rows_seats_per_row) < 3:
        return False, None, None, None
    try:
        title = " ".join(title_rows_seats_per_row[: len(title_rows_seats_per_row) - 2])
        rows = int(title_rows_seats_per_row[len(title_rows_seats_per_row) - 2])
        seats_per_row = int(title_rows_seats_per_row[len(title_rows_seats_per_row) - 1])
        if not title:
            return False, None, None, None
        if (
            rows <= 0
            or rows > consts.MAX_ROWS
            or seats_per_row <= 0
            or seats_per_row > consts.MAX_COLUMNS
        ):
            return False, None, None, None
        return True, title, rows, seats_per_row
    except ValueError:
        return False, None, None, None


def validate_menu_selection(selection_str: str) -> tuple:
    """Validate selection  of the menu.
    Args:
        selection_str (str): given input string
    Returns:
        a tuple values to indicate the selection of the menu is valid or not.
    """
    if selection_str is None or selection_str == "":
        return False, None
    return (True, selection_str) if selection_str in ["1", "2", "3"] else (False, None)


def validate_number_of_tickets(number_of_tickets_str: str) -> tuple:
    """Validate number of tickets string from input.
    Args:
        number_of_tickets_str (str): given input string
    Returns:
        a tuple values to indicate the number of tickets is valid or not.
    """
    if number_of_tickets_str is None or number_of_tickets_str == "":
        return False, None
    try:
        number_of_tickets = int(number_of_tickets_str)
        if number_of_tickets <= 0:
            return False, None
        return True, number_of_tickets
    except ValueError:
        return False, None


def validate_string_input(input_str: str) -> tuple:
    """Validate string input.
    Args:
        input_str (str): given string input
    Returns:
        a tuple values to indicate the string input is valid or not.
    """
    if input_str is None or input_str.strip() == "":
        return False, None
    return True, input_str
