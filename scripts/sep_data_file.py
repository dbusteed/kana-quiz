# run from root directory
#   ex: python scripts/sep_data_file.py

import csv
import os

DATA_PATH = 'data.csv'
DATA_DIR = 'data'
LINES_PER_FILE = 100

file_opened = False
dest_file = 0
writer = 0

with open(DATA_PATH) as src_file:
    reader = csv.reader(src_file)
    
    for i,line in enumerate(reader):

        file_num = i // LINES_PER_FILE

        if file_num % LINES_PER_FILE == 0:
            file_opened = False
            try:
                dest_file.close()
            except:
                pass
        
        if not file_opened:
            dest_file = open(os.path.join(DATA_DIR, f'data_part_{file_num}.csv'), 'a', newline='')
            writer = csv.writer(dest_file) 
        
        writer.writerows([line])