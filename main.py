# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import os

class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''



    def approximate_size(self, size1):
        '''Convert a file size to human-readable form.

       Keyword arguments:
       size -- file size in bytes
       a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                   if False, use multiples of 1000

       Returns: string

       '''
        SUFFIXES = {1024: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']}
        if size1 < 0:
            raise ValueError('number must be non-negative')

        multiple = 1024
        for suffix in SUFFIXES[multiple]:
            size1 /= multiple
            if size1 < multiple:
                return '{0:.1f} {1}'.format(size1, suffix)

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            size = os.path.getsize(self.pathname)
            size_new = self.approximate_size(size)
            self.tree += '    |' * n + '-' * 4 + self.pathname.name + '   ' + size_new  + '\n'
        elif self.pathname.is_dir():
            self.tree += '    |' * n + '-' * 4 + \
                         str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)


if __name__ == '__main__':
    dirtree = DirectionTree()
    # 命令参数个数为1，生成当前目录的目录树
    if len(sys.argv) == 1:
        dirtree.set_path(Path.cwd())
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为2并且目录存在存在
    elif len(sys.argv) == 2 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为3并且目录存在存在
    elif len(sys.argv) == 3 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        dirtree.set_filename(sys.argv[2])
        dirtree.save_file()
    else:  # 参数个数太多，无法解析
        print('命令行参数太多，请检查！')
