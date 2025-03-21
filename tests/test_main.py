from main import main


def test_booking_with_single_ticket(monkeypatch, capfd):
    inputs = iter(["Inception 8 10", "1", "4", "", "2", "GIC0001", "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    expected_outputs = [
        "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:",
        "Welcome to GIC Cinemas",
        "[1] Book tickets for Inception (80 seats available)",
        "[2] Check bookings",
        "[3] Exit",
        "Please enter your selection:",
        "Enter number of tickets to book, or enter blank to go back to main menu:",
        "Successfully reserved 4 Inception tickets.",
        "Booking id: GIC0001",
        "Selected seats:",
        "S C R E E N",
        "H . . . . . . . . . .",
        "G . . . . . . . . . .",
        "F . . . . . . . . . .",
        "E . . . . . . . . . .",
        "D . . . . . . . . . .",
        "C . . . . . . . . . .",
        "B . . . . . . . . . .",
        "A . . . o o o o . . .",
        "  1 2 3 4 5 6 7 8 9 10",
        "Enter blank to accept seat selection, or enter new seating position:",
        "Booking id: GIC0001 confirmed.",
        "[1] Book tickets for Inception (76 seats available)",
        "Enter booking id, or enter blank to go back to main menu:",
        "Thank you for using GIC Cinemas system. Bye!",
    ]
    main()
    output, err = capfd.readouterr()
    for line in expected_outputs:
        assert line in output


def test_booking_with_multiple_ticket(monkeypatch, capfd):
    inputs = iter(["Inception 8 10", "1", "4", "B03", "", "1", "77", "12", "B05", "", "2", "GIC0001", "GIC0002", "", "3"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    expected_outputs = [
        "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:",
        "Welcome to GIC Cinemas",
        "[1] Book tickets for Inception (80 seats available)",
        "[2] Check bookings",
        "[3] Exit",
        "Please enter your selection:",
        "Enter number of tickets to book, or enter blank to go back to main menu:",
        "Successfully reserved 4 Inception tickets.",
        "Booking id: GIC0001",
        "Selected seats:",
        "S C R E E N",
        "H . . . . . . . . . .",
        "G . . . . . . . . . .",
        "F . . . . . . . . . .",
        "E . . . . . . . . . .",
        "D . . . . . . . . . .",
        "C . . . . . . . . . .",
        "B . . . . . . . . . .",
        "A . . . o o o o . . .",
        "  1 2 3 4 5 6 7 8 9 10",
        "Enter blank to accept seat selection, or enter new seating position:",
        "B . . o o o o . . . .",
        "A . . . . . . . . . .",
        "Booking id: GIC0001 confirmed.",
        "[1] Book tickets for Inception (76 seats available)",
        "Sorry, there are only 76 seats available.",
        "Successfully reserved 12 Inception tickets.",
        "Booking id: GIC0002",
        "B . . # # # # o o . .",
        "A o o o o o o o o o o",
        "C . o o o o o o o o .",
        "B . . # # # # o o o o",
        "A . . . . . . . . . .",
        "Booking id: GIC0002 confirmed.",
        "[1] Book tickets for Inception (64 seats available)",
        "Enter booking id, or enter blank to go back to main menu:",
        "C . # # # # # # # # .",
        "B . . o o o o # # # #",
        "Thank you for using GIC Cinemas system. Bye!",
    ]
    main()
    output, err = capfd.readouterr()
    for line in expected_outputs:
        assert line in output
