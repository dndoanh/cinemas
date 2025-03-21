## GIC Cinemas Booking System
### Setup
To create and activate a new virtual environment, run the following commands:
#### Windows:
```commandline
python -m venv venv

.\venv\Scripts\activate
```
#### Linux:
```commandline
python -m venv venv

source venv/bin/activate
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
For linting, use `ruff`. To check the code, run the following command:
```commandline
ruff check
```
To format the code, run the following command: 
```commandline
ruff format
```
To format import, run the following command:
```commandline
ruff check --select I --fix
```
