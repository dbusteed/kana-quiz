# run from root directory
#   ex: python scripts/build_data_file.py

import csv
import os

DATA_PATH = 'data.csv'
DATA_DIR = 'data'

dest_file = open(DATA_PATH, 'a', newline='')
writer = csv.writer(dest_file)

for src_file in os.listdir(DATA_DIR):

    with open(os.path.join(DATA_DIR, src_file)) as f:
        reader = csv.reader(f)
        
        for line in reader:
            writer.writerows( [line] )

dest_file.close()
