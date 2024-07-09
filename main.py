import os
import time
import json
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from e6data_python_connector import Connection
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()

# Load environment variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
PORT = int(os.getenv('PORT', 80))
CATALOG = os.getenv('CATALOG', 'glue')


# Function to run a single query and return its metrics
def run_query(query, query_id, output_folder):
    conn = Connection(
        host=HOST,
        port=PORT,
        username=USERNAME,
        database=DATABASE,
        password=PASSWORD
    )
    cursor = conn.cursor(catalog_name=CATALOG)

    start_time = time.time()
    try:
        query_id = cursor.execute(query)
        all_records = cursor.fetchall()
        explain_response = cursor.explain_analyse()
        planner_result = json.loads(explain_response.get('planner'))
    except Exception as e:
        print(f"Error executing query {query_id}: {e}")
        cursor.clear()
        cursor.close()
        conn.close()
        return None

    end_time = time.time()

    parsing_time = planner_result.get("parsingTime")
    execution_time = planner_result.get("total_query_time") / 1000
    client_perceived_time = end_time - start_time
    row_count = cursor.rowcount

    # Save results to a file
    query_result_file = os.path.join(output_folder, f"{query_id}.txt")
    with open(query_result_file, 'w') as f:
        f.write(f"Query ID: {query_id}\n")
        f.write(f"Query Text: {query}\n")
        f.write(f"Parsing Time: {parsing_time} ms\n")
        f.write(f"Execution Time: {execution_time} s\n")
        f.write(f"Client Perceived Time: {client_perceived_time} s\n")
        f.write(f"Row Count: {row_count}\n")
        f.write(f"Results:\n")
        for record in all_records:
            f.write(f"{record}\n")

    cursor.clear()
    cursor.close()
    conn.close()

    return {
        'query_id': query_id,
        'query_text': query,
        'parsing_time': parsing_time,
        'execution_time': execution_time,
        'client_perceived_time': client_perceived_time,
        'row_count': row_count
    }


# Function to save the results to a CSV file
def save_results_to_csv(results, filename='benchmark_results.csv'):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)


# Function to calculate percentiles
def calculate_percentiles(data, percentiles):
    return np.percentile(data, percentiles)


def main():
    # Load queries from CSV file
    queries_df = pd.read_csv('queries.csv', header=None, names=['query_id', 'query_text'])
    queries = queries_df['query_text'].tolist()[:10]

    # Create output folder for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join('output', timestamp)
    os.makedirs(output_folder, exist_ok=True)

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_query = {executor.submit(run_query, query, queries_df['query_id'].iloc[i], output_folder): query for
                           i, query in enumerate(queries)}
        for future in as_completed(future_to_query):
            result = future.result()
            if result:
                results.append(result)

    # Save results to CSV
    save_results_to_csv(results, os.path.join(output_folder, 'benchmark_results.csv'))

    # Convert results to DataFrame for easier processing
    df = pd.DataFrame(results)

    # Calculate percentiles
    client_times = df['client_perceived_time']
    percentiles = [50, 90, 95, 99]
    percentile_values = calculate_percentiles(client_times, percentiles)

    for perc, value in zip(percentiles, percentile_values):
        print(f'P{perc}: {value}')

    # Find the top 5 slowest queries
    slowest_queries = df.nlargest(5, 'client_perceived_time')
    slowest_queries.to_csv(os.path.join(output_folder, 'slowest_queries.csv'), index=False)


if __name__ == '__main__':
    main()
