from functions.get_files_info import *
from functions.get_file_content import *


def main():

    print("Result for current directory:")
    print(get_file_content("calculator", "main.py"))

    print("Result for 'pkg' directory:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("Result for '/bin' directory:")
    print(get_file_content("calculator", "/bin/cat"))

    print("Result for '../' directory:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


main()