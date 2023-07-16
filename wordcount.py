import multiprocessing
import re
import sys
from collections import Counter

def count_words(filename, start, end):
    with open(filename, 'r') as file:
        file.seek(start)
        data = file.read(end - start)
        words = re.findall(r'\w+', data.lower())
    return Counter(words)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python3 program.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]


    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        with open(filename, 'r') as file:
            file_size = file.seek(0, 2)
            chunk_size = file_size // multiprocessing.cpu_count()

            results = []

            for i in range(multiprocessing.cpu_count()):
                start = i * chunk_size
                end = start + chunk_size if i < multiprocessing.cpu_count() - 1 else file_size
                results.append(pool.apply_async(count_words, (filename, start, end)))

            word_counts = Counter()

            for result in results:
                word_counts += result.get()

    merged_word_counts = Counter()
    for word, count in word_counts.items():
        merged_word_counts[word] += count
    counter_dict = dict(merged_word_counts)
    print(counter_dict)
