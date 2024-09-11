import collections
import re
import csv

file_path = 'combined_output.txt'
csv_output_file = 'top_30_common_words.csv'

word_count = collections.Counter()

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        words = re.findall(r'\b\w+\b', line.lower())
        word_count.update(words)

top_30_words = word_count.most_common(30)

print("Top 30 common words:")
for word, count in top_30_words:
    print(f"{word}: {count}")

with open(csv_output_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Word', 'Count'])
    writer.writerows(top_30_words)

print(f"Top 30 common words have been saved in {csv_output_file}")
