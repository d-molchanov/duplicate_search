from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileInfo():
    path: Path
    size: int
    atime: datetime
    mtime: datetime
    ctime: datetime
    btime: datetime | None



class FileInfoGetter:

    @staticmethod
    def get_file_info(path: Path) -> FileInfo:
        try:
            data = path.stat()
        except FileNotFoundError:
            raise

        try:
            birthtime = datetime.fromtimestamp(data.st_birthtimee)
        except AttributeError as e:
            birthtime = None

        result = FileInfo(
            path=path.resolve(),
            size=data.st_size,
            atime=datetime.fromtimestamp(data.st_atime),
            mtime=datetime.fromtimestamp(data.st_mtime),
            ctime=datetime.fromtimestamp(data.st_ctime),
            btime=birthtime
        )
        return result


def test():
    path = Path('./duplicates_searcher.py')
    # path = Path('./test.txt')
    fig = FileInfoGetter()
    try:
        file_info = fig.get_file_info(path)
        print(file_info)
    except FileNotFoundError:
        print(f'File not found: {path}')
    except PermissionError:
        print(f'Permission denied: {path}')




if __name__ == '__main__':
    test()