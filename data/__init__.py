import os
import json

def load_sample_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, 'sample_data.json')
    
    with open(data_file, 'r') as f:
        return json.load(f)

__all__ = ['load_sample_data']