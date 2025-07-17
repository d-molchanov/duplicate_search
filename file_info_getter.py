from pathlib import Path

class FileInfoGetter:

    def get_file_info(self, path: str | Path) -> dict:
        file_path = Path(path)
        data = file_path.stat()
        print(data)

def test():
    path = './duplicates_searcher.py'
    fig = FileInfoGetter()
    file_info = fig.get_file_info(path)

if __name__ == '__main__':
    test()