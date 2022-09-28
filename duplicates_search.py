import os
import time

if __name__ == '__main__':
	time_start = time.perf_counter()
	print('Hello!')
	total_time = time.perf_counter() - time_start
	print(
		f'Search has finished in {round(total_time*1e3, 3)} ms'
	)