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
2. Algorithm to generate seats reservation at specific position:
- Begin at the specified position (`start_row`, `start_col`) and reserve all available seats to the right of the cinema hall.
- If there are not enough seats available in the current row, proceed to the next row closer to the screen, reserving seats in a middle-most manner.
- If there are still not enough seats, return the `start_row` and continue reserving all seats available at the current row and next row further from the screen, again in a middle-most manner.
## Linting
Use `ruff` for linting. To check the code, run the following command:
```commandline
ruff check
```
To format the code, run the following command: 
```commandline
ruff format
```
To sort import, run the following command:
```commandline
ruff check --select I --fix
```
