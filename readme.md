# E6Data Query Benchmarking

This project is designed to run and benchmark multiple queries concurrently using Python. It uses the `multiprocessing` module to handle concurrency and the `e6data-python-connector` for interacting with the E6Data engine.

## Features

- Concurrent execution of queries using multiprocessing.
- Detailed benchmarking of query execution time, parsing time, and client perceived time.
- Error handling and logging for failed queries.
- Generation of benchmarking results with percentiles (P50, P90, P95, P99).
- Logging of the top 5 slowest queries.

## Project Structure

```
benchmarking_module/
├── src/
│ ├── init.py
│ ├── config.py
│ ├── query_runner.py
│ ├── utils.py
├── queries.csv
├── .env
├── main.py
```

- `src/config.py`: Loads configuration settings from the `.env` file.
- `src/query_runner.py`: Contains the function to run a query and handle exceptions.
- `src/utils.py`: Contains utility functions for saving results to CSV, calculating percentiles, and creating output folders.
- `queries.csv`: A CSV file containing the queries to be benchmarked.
- `.env`: Environment variables for the project.
- `main.py`: Main script to execute the benchmarking process.

## Prerequisites

- Python 3.6 or higher
- `pip` for installing Python packages

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd e6data-assignment
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install the required packages:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. **Create a virtual environment and activate it:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a .env file in the project root and add your configuration:**
   ```bash
   USERNAME=<your_username>
   PASSWORD=<your_password>
   HOST=<your_host>
   DATABASE=<your_database>
   PORT=80
   CATALOG=<your_catalog>
   ```
6**Prepare your queries.csv file with the following format:**
   ```bash
  query_id,query_text # (remove this line)
  TPCDS-13,"SELECT * FROM table WHERE condition;"
  TPCDS-48,"SELECT * FROM table WHERE condition;"
   ```

## Usage
To run the benchmarking process, execute the main script:
   ```bash
  python main.py
   ```
