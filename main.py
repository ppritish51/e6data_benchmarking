import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd

from src.config import load_config
from src.query_runner import run_query
from src.utils import save_results_to_csv, calculate_percentiles, create_output_folder


def main():
    config = load_config()

    # Load queries from CSV file
    queries_df = pd.read_csv('queries.csv', header=None, names=['query_id', 'query_text'])
    queries = queries_df['query_text'].tolist()

    # Create output folder for this run
    output_folder = create_output_folder()

    results = []

    print(f"Starting benchmark with {len(queries)} queries...")
    with ProcessPoolExecutor(max_workers=10) as executor:
        future_to_query = {executor.submit(run_query, query, queries_df['query_id'].iloc[i], output_folder, config): query for i, query in enumerate(queries)}
        completed_queries = 0
        for future in as_completed(future_to_query):
            result = future.result()
            if result:
                results.append(result)
                completed_queries += 1
                print(f"Completed {completed_queries}/{len(queries)} queries...")

    # Filter out failed queries
    successful_results = [res for res in results if res['client_perceived_time'] is not None]

    # Save results to CSV
    save_results_to_csv(successful_results, os.path.join(output_folder, 'benchmark_results.csv'))

    if successful_results:
        # Convert results to DataFrame for easier processing
        df = pd.DataFrame(successful_results)

        # Calculate percentiles
        client_times = df['client_perceived_time']
        percentiles = [50, 90, 95, 99]
        percentile_values = calculate_percentiles(client_times, percentiles)

        for perc, value in zip(percentiles, percentile_values):
            print(f'P{perc}: {value:.3f} ms')

        # Find the top 5 slowest queries
        slowest_queries = df.nlargest(5, 'client_perceived_time')
        slowest_queries.to_csv(os.path.join(output_folder, 'slowest_queries.csv'), index=False)

    print("Benchmarking completed.")

if __name__ == '__main__':
    main()
