import os
from datetime import datetime

import pandas as pd
import numpy as np


def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)


def calculate_percentiles(data, percentiles):
    return np.percentile(data, percentiles)


def create_output_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join('output', timestamp)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder
