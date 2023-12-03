import os
import time
from datetime import datetime
import hashlib
from argparse import ArgumentParser

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('dirs', nargs='+')

    return parser

class DuplicatesSeacher:
    
    def block_reader(self, file_obj, block_size):
        while True:
            block = file_obj.read(block_size)
            if not block:
                return
            yield block

    # Если передать неправильное имя файла, выбросит ошибку FileNotFoundError
    # def get_hash(self, filename, first_block_only):
    #     with open(filename, 'rb') as f:
    #         try:
    #             hash_obj = hashlib.sha1()
    #             if first_block_only:
    #                 hash_obj.update(f.read(1024))
    #             else:
    #                 for block in self.block_reader(f, 1024):
    #                     hash_obj.update(block)
    #             result = hash_obj.hexdigest().lower()
    #         except IOError:
    #             print(f'I/O error with {filename}')
    #             result = '-1'
    #     return result 

    def make_readable(self, size_in_bytes):
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

    
    def get_item_size(self, item_path):
        try:
            return os.path.getsize(item_path)
        except OSError:
            print(f'Error:\t<{item_path}> is not accessible')
            return None


    def get_paths(self, _root, _path):
        return [os.path.join(_root, p) for p in _path]


    def get_files_and_subdirs(self, dir: str):
        files = []
        subdirs = []
        for root, dirs, filenames in os.walk(dir):
            files += self.get_paths(root, filenames)
            subdirs += self.get_paths(root, dirs)
        return (files, subdirs)

    def get_directory_content(self, _dir: str):
        content = {'files': [], 'dirs': []}
        for root, dirs, filenames in os.walk(_dir):
            content['files'] += self.get_paths(root, filenames)
            content['dirs'] += self.get_paths(root, dirs)
        return content

    def get_directory_content_new(self, _dirs: list) -> dict:
        list_of_files = []
        list_of_dirs = []
        for d in _dirs:
            for root, dirs, filenames in os.walk(d):
                list_of_files.extend(self.get_paths(root, filenames))
                list_of_dirs.extend(self.get_paths(root, dirs))
        files = self.get_sizes_by_filenames(list_of_files)
        dirs = self.get_sizes_by_filenames(list_of_dirs)
        
        return {'files': self.remove_none_values(files),
                'dirs': self.remove_none_values(dirs)}

    def get_sizes_by_filenames(self, files):
        return {f: self.get_item_size(f) for f in files}


    def get_equal_files(self, list_of_files, key_function):
        result = dict()
        for f in list_of_files:
            key = key_function(f)
            if key in result:
                result[key].append(f)
            else:
                result[key] = [f]
        return result   


    def get_files_of_equal_hash(self, files_dict, function):
        result = dict()
        for value in files_dict.values():
            hash_dict = self.get_equal_files(value, function)
            for k, v in hash_dict.items():
                if k in result:
                    result[k] += v
                else:
                    result[k] = v
        return result
       

    def remove_items_with_one_value(self, input_dict):
        return {
            key: value for key, value in 
            input_dict.items() if len(value) > 1}     

    def get_count_and_size(self, input_dict):
        total_items_count = 0
        size_of_items = 0
        for key, value in input_dict.items():
            if key != None:
                items_count = len(value)
                total_items_count += items_count
                size_of_items += items_count*key
            else:
                print(f'Error:\t{key}:\t{value}')
        return (total_items_count, size_of_items)

    def get_item_hash(self, filename):
        with open(filename, 'rb') as f:
            try:
                block_size = 1024
                hash_obj = hashlib.sha1()
                for block in self.block_reader(f, block_size):
                    hash_obj.update(block)
                result = hash_obj.hexdigest().lower()
            except IOError:
                print(f'I/O error with {filename}')
                result = '-1'
        return result


    def get_first_block_hash(self, filename):
        with open(filename, 'rb') as f:
            try:
                first_block = 1024
                hash_obj = hashlib.sha1()
                hash_obj.update(f.read(first_block))
                result = hash_obj.hexdigest().lower()
            except IOError:
                print(f'I/O error with {filename}')
                result = '-1'
        return result


    def get_directory_info(self, dir, files: dict, dirs: dict):
        result = {'directory': os.path.abspath(dir)}
        (
            result['files_count'],
            result['size_of_files']
        ) = self.get_count_and_size(files)
        (
            result['dirs_count'], 
            result['size_of_dirs']
            ) = self.get_count_and_size(dirs)
        return result

    # def get_directory_info_new(self, files: dict, dirs: dict)

    def print_dict(self, input_dict):
        for i, (k, v) in enumerate(input_dict.items()):
            print(f'{i+1}:\t{k}\t{v}')

    def get_count_and_sizes_of_duplicates(
        self, input_dict: dict, dict_with_sizes: dict):
        total_size = 0
        count = 0
        for value in input_dict.values():
            amount = len(value)
            count += amount
            total_size += (dict_with_sizes[value[0]]*amount)
        return (count, total_size)


    def print_duplicates_info(self, duplicates: dict, 
        sizes_by_files: dict, dir_info: dict, title: str):
        dc, ds = self.get_count_and_sizes_of_duplicates(
            duplicates, sizes_by_files)
        print('{0}\t\t{1} / {2} / {3} %'.format(
            title, dc, self.make_readable(ds), 
            round(ds/dir_info['size_of_files']*100, 2)))

    def print_duplicates_info_new(self, duplicates: dict, 
        sizes_by_files: dict, size_of_files: int, title: str):
        dc, ds = self.get_count_and_sizes_of_duplicates(
            duplicates, sizes_by_files)
        print('{0}\t\t{1} / {2} / {3} %'.format(
            title, dc, self.make_readable(ds), 
            round(ds/size_of_files*100, 2)))

    def print_dir_info(self, dir_info):
        print(f'Current directory:\t\t<{dir_info["directory"]}>')
        dir_info['items_count'] = (
            dir_info['files_count'] + dir_info['dirs_count'])
        dir_info['size_of_items'] = (
            dir_info['size_of_files'] + dir_info['size_of_dirs'])
        print(' / '.join((
            f'Files:\t\t\t\t\t{dir_info["files_count"]}',
            f'{self.make_readable(dir_info["size_of_files"])}')))
        print(' / '.join((
            f'Directories:\t\t\t{dir_info["dirs_count"]}',
            f'{self.make_readable(dir_info["size_of_dirs"])}')))
        print(' / '.join((
            f'Total items:\t\t\t{dir_info["items_count"]}',
            f'{self.make_readable(dir_info["size_of_items"])}')))

    def sort_files_by_size(self, input_dict: dict, sizes_by_files: dict):
        return {sizes_by_files[v[0]]:v for v in input_dict.values()}

    def write_dictionary_to_file(self, input_dict: dict, filename: str):
        keys = sorted(list(input_dict.keys()), reverse=True)
        try:
            with open(filename, 'w') as w:
                for k in keys:
                    for value in sorted(input_dict[k], reverse=True):
                        w.write(f'{k}\t{value}\n')
        except IOError:
            print(f'IOError with <{filename}>: cannot write data.')

    def get_files_to_remove(self, duplicates: dict):
        return {k:sorted(v, reverse=True)[1:] for 
        k, v in duplicates.items()}

    def remove_files(self, files: dict):
        temp_list = [f for value in files.values() for f in value]
        if temp_list:
            files_to_remove = sorted(temp_list)
            for f in files_to_remove:
                try:
                    os.remove(f)
                except FileNotFoundError:
                    print(f'FileNotFoundError with <{f}>: no such file or directory.')

    def print_info_for_removing_files(self, files: dict, 
        sizes_by_files: dict):
        temp = dict()
        for key, value in files.items():
            size = sizes_by_files[value[0]]
            if size in temp:
                temp[size] += (key, value)
            else:
                temp[size] = [(key, value)]
        sizes = sorted(temp.keys(), reverse=True)
        result = []
        for s in sizes:
            for k, value in temp[s]:
                for v in value:
                    result.append(f'{s}\t{k}\t{v}')
        return '\n'.join(result)
        
    # def find_duplicates(self, files: list):
    #     sizes_by_files = self.get_sizes_by_filenames(files)
    #     files_by_size = self.get_equal_files(files, self.get_item_size)
    #     dirs_by_size = self.get_equal_files(subdirs, self.get_item_size)
    #     dir_info = self.get_directory_info(_dir, files_by_size, dirs_by_size)
    #     self.print_dir_info(dir_info)
        
    #     duplicates_by_size = self.remove_items_with_one_value(files_by_size)
    #     self.print_duplicates_info(duplicates_by_size, sizes_by_files, 
    #         dir_info, 'Duplicates by size:')

    #     files_by_first_block_hash = self.get_files_of_equal_hash(
    #         duplicates_by_size, self.get_first_block_hash)
    #     duplicates_by_first_block_hash = self.remove_items_with_one_value(
    #         files_by_first_block_hash)
    #     self.print_duplicates_info(
    #         duplicates_by_first_block_hash, sizes_by_files, 
    #         dir_info, 'Duplicates by 1kB:')

    #     files_by_hash = self.get_files_of_equal_hash(
    #         duplicates_by_first_block_hash, self.get_item_hash)
    #     duplicates_by_hash = self.remove_items_with_one_value(files_by_hash)
    #     self.print_duplicates_info(duplicates_by_hash, sizes_by_files, 
    #         dir_info, 'Duplicates by hash:')
        
     
    #     files_to_remove = self.get_files_to_remove(duplicates_by_hash)
    #     self.print_duplicates_info(files_to_remove, sizes_by_files, 
    #         dir_info, 'Files to remove:')

    #     return files_to_remove
        
    def find_duplicates_new(self, sizes_by_files: dict):

        files_by_size = dict()
        for key, value in sizes_by_files.items():
            if value in files_by_size:
                files_by_size[value].append(key)
            else:
                files_by_size[value] = [key]

        
        duplicates_by_size = self.remove_items_with_one_value(files_by_size)

        files_by_first_block_hash = self.get_files_of_equal_hash(
            duplicates_by_size, self.get_first_block_hash)
        duplicates_by_first_block_hash = self.remove_items_with_one_value(
            files_by_first_block_hash)

        files_by_hash = self.get_files_of_equal_hash(
            duplicates_by_first_block_hash, self.get_item_hash)
        duplicates_by_hash = self.remove_items_with_one_value(files_by_hash)
        
        # duplicates = {(k, sizes_by_files[v[0]]): v for k, v in duplicates_by_hash.items()}
        duplicates = dict()
        for key, value in duplicates_by_hash.items():
            if sizes_by_files[value[0]] in duplicates:
                duplicates[sizes_by_files[value[0]]].append({key:value})
            else:
                duplicates[sizes_by_files[value[0]]] = [{key:value}]

        # return duplicates_by_hash
        # for key, value in duplicates.items():
        #     print(key, end='\t')
        #     for v in value:
        #         for i, j in v.items():
        #             print(i)
        #             for a in j:
        #                 print(f'\t{a}')
        print(duplicates)
        return duplicates

    def get_duplicates_to_remove(self, duplicates: dict) -> dict:
        result = dict()
        for size, dicts in duplicates.items():
            result[size] = []
            for d in dicts:
                temp_d = dict()
                for _hash, _path in d.items():
                    temp_d[_hash] = _path[1:]
                result[size].append(temp_d)
        return result

    #Зачем вообще нужен этот метод?
    def remove_none_values(self, input_dict: dict):
        return {key: value for key, value in 
            input_dict.items() if value != None}


    def find_duplicates_in_directory(self, _dirs: list):
        dir_content = self.get_directory_content_new(_dirs)
        files = dir_content['files']
        files_count = len(dir_content['files'])
        size_of_files = sum(list(dir_content['files'].values()))

        dirs_count = len(dir_content['dirs'])
        size_of_dirs = sum(list(dir_content['dirs'].values()))

        items_count = files_count + dirs_count
        size_of_items = size_of_files + size_of_dirs

        # print(f'Current directory:\t\t{os.path.abspath(_dir)}')
        print(' / '.join((
            f'Files:\t\t\t\t\t{files_count}',
            f'{self.make_readable(size_of_files)}')))
        print(' / '.join((
            f'Directories:\t\t\t{dirs_count}',
            f'{self.make_readable(size_of_dirs)}')))
        print(' / '.join((
            f'Total items:\t\t\t{items_count}',
            f'{self.make_readable(size_of_items)}')))

        duplicates = self.find_duplicates_new(files)
        # self.print_duplicates_info_new(duplicates, files, 
        #     size_of_files, 'Duplicates:\t\t')

        return duplicates
        
    def create_report(self, duplicates, filename):
        # sizes = sorted(duplicates, reverse=True)
        # sizes = sorted(list(duplicates.keys()), reverse=True)
        with open(filename, 'w') as f:
            # for s in sizes:
            for s in sorted(duplicates, reverse=True):
                for d in duplicates[s]:
                    for key, value in d.items():
                        # value = sorted(value, reverse=True)
                        for v in value:
                            f.write(f'{key};{self.make_readable(s)};{v}\n')

    def create_list_for_deleting(self, duplicates, filename, detailed=False):
        if duplicates:
            sizes = sorted(list(duplicates.keys()), reverse=True)
            duplicates_for_deleting = 0
            free_space = 0
            with open(filename, 'w') as f:
                if detailed:
                    for s in sizes:
                        for d in duplicates[s]:
                            for key, value in d.items():
                                dfd = len(value) - 1
                                duplicates_for_deleting += dfd
                                free_space += s*dfd
                                value = sorted(value, reverse=True)
                                for v in value[1:]:
                                    f.write(f'{key};{self.make_readable(s)};{v}\n')
                    if sizes[-1] == 0:
                        key = list(duplicates[0][0].keys())[0]
                        v = sorted(duplicates[0][0][key], reverse=True)[0]
                        f.write(f'{key};{self.make_readable(0)};{v}\n')        
                else:
                    for s in sizes:
                        for d in duplicates[s]:
                            for key, value in d.items():
                                dfd = len(value) - 1
                                duplicates_for_deleting += dfd
                                free_space += s*dfd
                                value = sorted(value, reverse=True)
                                for v in value[1:]:
                                    f.write(f'{v}\n')
                    if sizes[-1] == 0:
                        key = list(duplicates[0][0].keys())[0]
                        v = sorted(duplicates[0][0][key], reverse=True)[0]
                        duplicates_for_deleting += 1
                        f.write(f'{v}\n')
            print(' / '.join((
                f'Items for deleting:\t\t{duplicates_for_deleting}',
                f'{self.make_readable(free_space)}')))
        else:
            print('There is no file for deleting')

    def create_report_2(self, duplicates, filename):
        sizes = sorted(list(duplicates.keys()), reverse=True)
        with open(filename, 'w') as f:
            for s in sizes:
                for d in duplicates[s]:
                    for key, value in d.items():
                        f.write(f'{key};{self.make_readable(s)}\n')
                        value = sorted(value, reverse=True)
                        for v in value:
                            f.write(f'{v}\n')

    def remove_empty_directories(self, target_dir: str):
        there_are_empty_directories = True
        while there_are_empty_directories:
            count = 0
            for root, dirs, filenames in os.walk(target_dir, topdown=False):
                print(count, root)
                if not filenames and not dirs:
                    try:
                        # os.rmdir(root)
                        # count += 1
                        # print(root)
                        pass
                    except OSError:
                        print('{0} {1}'.format(f'OSError with {root}:'
                            ' directrory is not empty.'))
                    except FileNotFoundError:
                        print('{0} {1}'.format(
                            f'FileNotFoundError with {root}:',
                            ' directory does not exist.'))
            print(f'{count} directories have been removed.')
            if count == 0:
                there_are_empty_directories = False


if __name__ == '__main__':

    argparser = create_parser()
    args = argparser.parse_args(['./test', './test (копия)'])
    # args = argparser.parse_args(['./test'])
    print('This is a program for duplicates searching. Directories for searching:\n')
    target_dirs = args.dirs
    for d in target_dirs:
        print(os.path.abspath(d))
    # time_start = time.perf_counter()
    ds = DuplicatesSeacher()
    duplicates = ds.find_duplicates_in_directory(target_dirs)
    ds.create_report(duplicates, 'duplicates.csv')
    ds.create_list_for_deleting(duplicates, 'deleting.csv', detailed=True)
    duplicates_to_remove = ds.get_duplicates_to_remove(duplicates)
    ds.create_report(duplicates_to_remove, 'd_to_remove.csv')
    # total_time = time.perf_counter() - time_start
    # print(
    #     f'Search has finished in {round(total_time*1e3, 3)} ms')
    # time_start = time.perf_counter()
    # # ds.remove_duplicates('output.csv', '\t')
    # total_time = time.perf_counter() - time_start
    # print(
    #     f'Removing of duplicates has finished in {round(total_time*1e3, 3)} ms'
    # )
    # time_start = time.perf_counter()
    # ds.remove_empty_directories(target_dir)
    # total_time = time.perf_counter() - time_start
    # print(
    #     f'Removing of empty directories has finished in {round(total_time*1e3, 3)} ms'
    # )