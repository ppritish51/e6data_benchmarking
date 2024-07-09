# E6Data Query Benchmarking

This project is designed to run and benchmark multiple queries concurrently using Python. It uses the `multiprocessing` module to handle concurrency and the `e6data-python-connector` for interacting with the E6Data engine.

## Features

- Concurrent execution of queries using multiprocessing.
- Detailed benchmarking of query execution time, parsing time, and client perceived time.
- Error handling and logging for failed queries.
- Generation of benchmarking results with percentiles (P50, P90, P95, P99).
- Logging of the top 5 slowest queries.

## Project Structure

benchmarking_module/
├── src/
│ ├── init.py
│ ├── config.py
│ ├── query_runner.py
│ ├── utils.py
├── queries.csv
├── .env
├── main.py


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
