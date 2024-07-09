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
├── output/
│ ├── <timestamp>/
│ ├── benchmark_results.csv
│ ├── slowest_queries.csv
│ ├── error_queries/
│ │ ├── <query_id>.txt
│ ├── <query_id>.txt
├── queries.csv
├── .env
├── main.py
```

- `src/config.py`: Loads configuration settings from the `.env` file.
- `src/query_runner.py`: Contains the function to run a query and handle exceptions.
- `src/utils.py`: Contains utility functions for saving results to CSV, calculating percentiles, and creating output folders.
- `output/`: Contains subfolders for each run, named with the current timestamp.
  - `<timestamp>/`: A folder created for each run, named with the current timestamp.
    - `benchmark_results.csv`: Contains the results of the benchmark.
    - `slowest_queries.csv`: Contains the top 5 slowest queries.
    - `error_queries/`: Contains error logs for failed queries.
      - `<query_id>.txt`: Contains error details for the failed query.
    - `<query_id>.txt`: Contains the results of each query.
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
6. **Prepare your queries.csv file with the following format:**
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

## Output
1. A new folder will be created inside the output directory for each run, named with the current timestamp.
2. Each query's results are saved in a text file named after the query ID.
3. Benchmark results are saved in benchmark_results.csv inside the output folder.
4. The top 5 slowest queries are saved in slowest_queries.csv inside the output folder.
5. Any errors encountered during query execution are logged in a separate error_queries folder inside the output folder.
