import os
import time
from datetime import datetime
import hashlib
from argparse import ArgumentParser
from itertools import permutations
from duplicates_searcher import DuplicatesSeacher
from pathlib import Path

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('dirs', nargs='+')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove found duplicates.')

    return parser




if __name__ == '__main__':

    argparser = create_parser()
    # args = argparser.parse_args(['./test', './test (копия)', '-r'])
    # args = argparser.parse_args(['./test'])
    # args = argparser.parse_args(['./test', './test (копия)'])
    args = argparser.parse_args(['./test', './test (копия)', '/'])
    # args = argparser.parse_args(['./test/1', './test', '/'])
    print(args)

    ds = DuplicatesSeacher()
    # ds.set_directories(args.dirs)
    paths = [Path('.'), Path('../..'), Path('~'), Path('/'), Path('*')]
    
    resolved_paths = [p.resolve() for p in paths]
    print(*resolved_paths, sep='\n')
    print(*[p.resolve() for p in paths], sep='\n')
    print(*[p.exists() for p in paths], sep='\n')
    print(*[p.is_absolute() for p in paths], sep='\n')
    print(Path('/home/test1/test2').is_relative_to(Path('/home/test3')))
    print([p for p in Path('/home/test1/test2').parents])
    ds.directories = args.dirs
    # ds.get_directories_content_new(ds.directories)
    # print(len(Path('/home')))
    all_files = ds.get_all_files(ds.directories)
    print(*all_files, sep='\n')

    # argparser = create_parser()
    # #Нужно сделать проверку, что директории не являются вложенными (или идентичными)
    # # args = argparser.parse_args(['./test', './test (копия)', '-r'])
    # args = argparser.parse_args(['./test', './test (копия)'])
    # print(args)
    # print('This is a program for duplicates searching. Directories for searching:\n')
    # ds = DuplicatesSeacher()
    # target_dirs = ds.get_individual_paths(args.dirs)
    # for d in target_dirs:
    #     print(os.path.abspath(d))
    # # time_start = time.perf_counter()
    # duplicates = ds.find_duplicates_in_directories(target_dirs)
    
    # rd = False
    # if args.remove:
    #     rd = True
    #     # ds.remove_duplicates(duplicates_to_remove)
    #     # for d in target_dirs:
    #     #     ds.remove_empty_directories(d)
    
    # ds.list_duplicates(target_dirs, duplicates, remove_duplicates=rd)
    # # ======================old============================
    # # total_time = time.perf_counter() - time_start
    # # print(
    # #     f'Search has finished in {round(total_time*1e3, 3)} ms')
    # # time_start = time.perf_counter()
    # # # ds.remove_duplicates('output.csv', '\t')
    # # total_time = time.perf_counter() - time_start
    # # print(
    # #     f'Removing of duplicates has finished in {round(total_time*1e3, 3)} ms'
    # # )
    # # time_start = time.perf_counter()
    # # ds.remove_empty_directories(target_dir)
    # # total_time = time.perf_counter() - time_start
    # # print(
    # #     f'Removing of empty directories has finished in {round(total_time*1e3, 3)} ms'
    # # )