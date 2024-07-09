import os
import time
import json
from e6data_python_connector import Connection
import grpc

def run_query(query, query_id, output_folder, config):
    print(f"Starting query {query_id}...")
    conn = Connection(
        host=config['HOST'],
        port=config['PORT'],
        username=config['USERNAME'],
        database=config['DATABASE'],
        password=config['PASSWORD']
    )
    cursor = conn.cursor(catalog_name=config['CATALOG'])

    start_time = time.time()
    try:
        cursor.execute(query)
        all_records = cursor.fetchall()
        explain_response = cursor.explain_analyse()
        planner_result = json.loads(explain_response.get('planner'))
    except grpc.RpcError as e:
        error_message = f"Error executing query {query_id}: {e.details()}"
        print(error_message)
        error_folder = os.path.join(output_folder, 'error_queries')
        os.makedirs(error_folder, exist_ok=True)
        with open(os.path.join(error_folder, f"{query_id}.txt"), 'w') as f:
            f.write(f"Query ID: {query_id}\n")
            f.write(f"Query Text: {query}\n")
            f.write(f"Error: {e.details()}\n")
        cursor.clear()
        cursor.close()
        conn.close()
        return {
            'query_id': query_id,
            'parsing_time': None,
            'execution_time': None,
            'client_perceived_time': None,
            'row_count': None,
            'error': e.details()
        }
    except Exception as e:
        error_message = f"Error executing query {query_id}: {str(e)}"
        print(error_message)
        error_folder = os.path.join(output_folder, 'error_queries')
        os.makedirs(error_folder, exist_ok=True)
        with open(os.path.join(error_folder, f"{query_id}.txt"), 'w') as f:
            f.write(f"Query ID: {query_id}\n")
            f.write(f"Query Text: {query}\n")
            f.write(f"Error: {str(e)}\n")
        cursor.clear()
        cursor.close()
        conn.close()
        return {
            'query_id': query_id,
            'parsing_time': None,
            'execution_time': None,
            'client_perceived_time': None,
            'row_count': None,
            'error': str(e)
        }

    end_time = time.time()

    parsing_time = planner_result.get("parsingTime")
    execution_time = planner_result.get("total_query_time")
    client_perceived_time = (end_time - start_time) * 1000  # Convert to milliseconds
    row_count = cursor.rowcount

    # Save results to a file
    query_result_file = os.path.join(output_folder, f"{query_id}.txt")
    with open(query_result_file, 'w') as f:
        f.write(f"Query ID: {query_id}\n")
        f.write(f"Parsing Time: {parsing_time:.3f} ms\n")
        f.write(f"Execution Time: {execution_time:.3f} ms\n")
        f.write(f"Client Perceived Time: {client_perceived_time:.3f} ms\n")
        f.write(f"Row Count: {row_count}\n")
        # f.write(f"Results:\n")
        # for record in all_records:
        #     f.write(f"{record}\n")

    cursor.clear()
    cursor.close()
    conn.close()

    print(f"Completed query {query_id}.")

    return {
        'query_id': query_id,
        'parsing_time': parsing_time,
        'execution_time': execution_time,
        'client_perceived_time': client_perceived_time,
        'row_count': row_count,
        'error': None
    }
