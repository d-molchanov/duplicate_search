import os
import time

class DuplicatesSeacher:
    def search(self, dir):
        print('Start searching\n...')
    

if __name__ == '__main__':
    time_start = time.perf_counter()
    print('This is program for duplicates searching.')
    total_time = time.perf_counter() - time_start
    ds = DuplicatesSeacher()
    ds.search('.')
    print(
        f'Search has finished in {round(total_time*1e3, 3)} ms'
    )