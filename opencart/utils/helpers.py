from mimesis import Person
import os
import glob
import time

class Client:
    _person = Person()

    def __init__(self):
        self.__type = "Client"
        self.first_name = self._person.name()
        self.last_name = self._person.surname()
        self.email = self._person.email()
        self.password = self._person.password()
        self.phone_number = self._person.phone_number()



relative_path = 'screenshots'
absolute_path = os.path.abspath(relative_path)
path_src = os.path.join(absolute_path, f"screenshot_{time.strftime("%Y%m%d-%H%M%S")}.png")  # путь к скринам
# print(f"path_src - {path_src}")


# path_inputfiles = os.path.dirname(os.path.abspath("screenshots"))  # путь к папке "files"
# files_dir = os.listdir(path_inputfiles)  # список имен фалов в папке "screenshots"
# path_src = os.path.join(path_inputfiles, f"screen_{time.strftime("%Y%m%d-%H%M%S")}.png")  # путь к архиву

# def clear_dir():
#     '''
#     func: delete all files from dir with archive
#     '''
#     all_files = os.path.join(path_inputfiles, '*.*')
#     for file in glob.glob(all_files):
#         os.remove(file)

