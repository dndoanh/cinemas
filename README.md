## GIC Cinemas Booking System
### Setup
To create and activate a new virtual environment, run the following commands:
```commandline
python -m venv venv

.\venv\Scripts\activate
```
To install the necessary Python packages (include `--trusted-host` if required), run:
```commandline
pip install -r requirements.txt
```
## How to run
To run the code, use following command:
```commandline
python -m main
```
## Testing
To run unit tests, use:
```commandline
pytest .
```
To run unit tests with coverage, use:
```commandline
pytest --cov .
```
## Assumptions
1. Upon invalid input (e.g. invalid movie title rows, seats per row; invalid number of tickets, invalid of seating position, invalid booking id), the program will prompt an error message for input again.
## Linting
For linting, use `black`, `isort` and `flake8`. To format the code, run the following commands:
```commandline
black --line-length=160 .

isort --profile=black --line-length=160 .

flake8 .
```

