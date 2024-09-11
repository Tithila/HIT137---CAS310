import os
import csv

output_file = 'output.txt'

with open(output_file, 'w', encoding='utf-8') as txt_file:
    for filename in os.listdir():
        if filename.endswith('.csv'):
            with open(filename, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    txt_file.write(' '.join(row) + '\n')

print(f"Text extracted from all CSV files in the current directory and saved to {output_file}")
