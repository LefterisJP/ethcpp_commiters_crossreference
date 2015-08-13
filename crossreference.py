#!/usr/bin/python
import sys
import os
import subprocess

authors = [
    'guanqun.lu@gmail.com',
    'daniel.hams@gmail.com',
    'elombrozo@gmail.com',
    'josephyzhou@gmail.com',
    'markobarko@gmail.com',
]

ignored_dirs = ['.git', 'build']


def topdir(p):
    d = temp = os.path.dirname(p)
    while temp and not (temp == '' or temp == '.'):
        d = os.path.dirname(d)
        temp = os.path.dirname(d)
    return d

def dirty_files(cpp_path):
    os.chdir(cpp_path)
    string_set = set()
    for author in authors:
        slist = subprocess.Popen("git log --no-merges --stat --author={} --name-only --pretty=format:"" | sort -u".format(author),
                                 shell=True,
                                 stdout=subprocess.PIPE).stdout.read()
        string_set = string_set.union(set(slist.split('\n')))
    return string_set


def find_files(cpp_path):
    files_set = set()
    for subdir, dirs, files in os.walk(cpp_path):
        while '.git' in dirs:
            dirs.remove('.git')
        while 'build' in dirs:
            dirs.remove('build')
        for file in files:
            files_set.add(os.path.join(subdir, file))
    return files_set

if __name__ == "__main__":
    arg_num = len(sys.argv)
    cpp_path = "."

    if arg_num == 2:
        cpp_path = sys.argv[1]
    elif arg_num == 1:
        print("Usage:\n\tcrossreference.py CPPETHEREUM-PATH")
        sys.exit(1)
    else:
        print("Incorrect number of arguments given {}".format(arg_num))
        sys.exit(1)

    if not os.path.exists(cpp_path):
        print("Given path for cpp-ethereum \"{}\" does not exist.".format(
            cpp_path)
        )

    dirtyf = dirty_files(cpp_path)
    allf = find_files(cpp_path)
    cleanf = allf.difference(dirtyf)

    print("This is a list of files touched only by people who have signed\n\n")
    flist = list(cleanf)
    flist.sort()
    for f in flist:
        print(f)
