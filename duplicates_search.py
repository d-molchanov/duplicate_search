import os
import time
import hashlib

class DuplicatesSeacher:
    def block_reader(self, file_obj, block_size):
        while True:
            block = file_obj.read(block_size)
            if not block:
                return
            yield block

    # Если передать неправильное имя файла, выбросит ошибку FileNotFoundError
    def get_hash(self, filename, first_block_only):
        with open(filename, 'rb') as f:
            try:
                hash_obj = hashlib.sha1()
                if first_block_only:
                    hash_obj.update(f.read(1024))
                else:
                    for block in self.block_reader(f, 1024):
                        hash_obj.update(block)
                result = hash_obj.hexdigest().lower()
            except IOError:
                print(f'I/O error with {filename}')
                result = '-1'
        return result 

    def search(self, list_of_files):
        # print('Start searching for duplicates\n...')
        if len(list_of_files) < 2:
            return None
        else:
            duplicates = dict()
            hash_1kB = dict()
            hash_total = dict()
            for filename in list_of_files:
                continue
            return duplicates

    def search_hash_1kB(self, list_of_files):
        data = dict()
        for filename in list_of_files:
            hash_obj = self.get_hash(filename, True)
            if hash_obj in data:
                data[hash_obj].append(filename)
            else:
                data[hash_obj] = [filename]
        one_value = []
        for key, value in data.items():
            if len(value) < 2:
                one_value.append(key)
        for key in one_value:
            data.pop(key)
        return data

    def search_hash(self, list_of_files):
        data = dict()
        for filename in list_of_files:
            hash_obj = self.get_hash(filename, False)
            if hash_obj in data:
                data[hash_obj].append(filename)
            else:
                data[hash_obj] = [filename]
        one_value = []
        for key, value in data.items():
            if len(value) < 2:
                one_value.append(key)
        for key in one_value:
            data.pop(key)
        return data

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
                    print(f'Error:\t<{filename}> is not accessible')
        one_value = []
        for key, value in data.items():
            if len(value) < 2:
                one_value.append(key)
        for key in one_value:
            data.pop(key)
        return data

    def __make_readable(self, size_in_bytes):
        if size_in_bytes == 0:
            return '0 B'
        n = size_in_bytes
        number_of_digits = 0
        while n > 0:
            n //= 10
            number_of_digits += 1
        if number_of_digits > 15:
            return f'{round(size_in_bytes / 10**15, 3)} PB'
        elif number_of_digits > 12:
            return f'{round(size_in_bytes / 10**12, 3)} TB'
        elif number_of_digits > 9:
            return f'{round(size_in_bytes / 10**9, 3)} GB'
        elif number_of_digits > 6:
            return f'{round(size_in_bytes / 10**6, 3)} MB'
        elif number_of_digits > 3:
            return f'{round(size_in_bytes / 10**3, 3)} kB'
        else:
            return f'{size_in_bytes} B'


    def get_directory_info(self, dir):
        target_dir = os.path.abspath(dir)
        print(f'Scanning:\t\t<{target_dir}>')
        amount_of_files = 0
        amount_of_dirs = 0
        total_size_of_files = 0
        total_size_of_dirs = 0
        for root, dirs, filenames in os.walk(dir):
            for f in filenames:
                file_path = os.path.join(root, f)
                try:
                    file_size = os.path.getsize(file_path)
                    amount_of_files += 1
                    total_size_of_files += file_size
                except OSError:
                    print(f'Error:\t<{file_path}> is not accessible')
            for d in dirs:
                dir_path = os.path.join(root, d)
                try:
                    dir_size = os.path.getsize(dir_path)
                    amount_of_dirs += 1
                    total_size_of_dirs += dir_size
                except OSError:
                    print(f'Error:\t<{dir_path}> is not accessible')

        amount_of_items = amount_of_files + amount_of_dirs
        total_size_of_items = total_size_of_files + total_size_of_dirs
        
        print(' / '.join((
                    f'Files:\t\t\t{amount_of_files}',
                    f'{self.__make_readable(total_size_of_files)}')))
        print(' / '.join((
            f'Directories:\t{amount_of_dirs}',
            f'{self.__make_readable(total_size_of_dirs)}')))
        print(' / '.join((
            f'Total items:\t{amount_of_items}',
            f'{self.__make_readable(total_size_of_items)}')))



if __name__ == '__main__':
    time_start = time.perf_counter()
    print('This is a program for duplicates searching.')
    ds = DuplicatesSeacher()
    ds.get_directory_info('./JIHT')
    # ds.get_directory_info('./test')
    # files = ds.search_same_size('./JIHT')

    # hash_1kB = dict()
    # for el in files.keys():
    #     temp_dict = ds.search_hash_1kB(files[el])
    #     for key, value in temp_dict.items():
    #         hash_1kB[key] = value

    # hash_total = dict()
    # for el in hash_1kB.keys():
    #     temp_dict = ds.search_hash(hash_1kB[el])
    #     for key, value in temp_dict.items():
    #         hash_total[key] = value

    # hash_size = dict()
    # available_space = 0
    # for key, value in hash_total.items():
    #     size_of_file = os.path.getsize(value[0])
    #     available_space += size_of_file*(len(value) - 1)
    #     hash_size[size_of_file] = key
    # file_sizes = list(hash_size.keys())
    # file_sizes.sort()
    # file_sizes.reverse()
    # with open('log.csv', 'w') as w:
    #     for s in file_sizes:
    #         w.write(f'{s};{hash_size[s]}\n')
    #         for el in hash_total[hash_size[s]]:
    #             w.write(f';{el}\n')
    # print(f'Available space:\t{round(available_space/2**30, 3)} GiB')
    total_time = time.perf_counter() - time_start
    print(
        f'Search has finished in {round(total_time*1e3, 3)} ms'
    )