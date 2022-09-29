import os
import time
import hashlib

class DuplicatesSeacher:
    def read_block(file_obj, block_size):
        while True:
            block = file_obj.read(block_size)
            if not block:
                return
            yield block

    def search(self, list_of_files):
        print('Start searching for duplicates\n...')
        duplicates = dict()
        for filename in list_of_files:
            with open(filename, 'rb') as f:
                try:
                    hash_func = hashlib.sha1()
                    first_block = read_block(f, 1024)
                    hash_func.update(first_block)
                    if hash_func.hexdigit().lower() in duplicates:
                        continue
                    else:
                        pass
                except IOError:
                    print(f'I/O error with {filename}')

        for el in os.walk(dir):
            for filename in el[-1]:
                file_path = os.path.join(el[0], filename)
                file_size = os.path.getsize(file_path)
                if file_size in data:
                    duplicates[file_size].append(file_path)
                else:
                    duplicates[file_size] = [file_path]
        return duplicates

    def search_same_size(self, dir):
        data = dict()
        for el in os.walk(dir):
            for filename in el[-1]:
                file_path = os.path.join(el[0], filename)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size in data:
                        data[file_size].append(file_path)
                    else:
                        data[file_size] = [file_path]
                except OSError:
                    continue
        return data

if __name__ == '__main__':
    time_start = time.perf_counter()
    print('This is program for duplicates searching.')
    total_time = time.perf_counter() - time_start
    ds = DuplicatesSeacher()
    files = ds.search_same_size('./test')
    for key, value in files.items():
        print(f'{key}:\t{value}')
    print(
        f'Search has finished in {round(total_time*1e3, 3)} ms'
    )