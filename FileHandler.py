from os.path import abspath, join, dirname

MAIN_PATH = dirname(__file__)

def FileWriter(file_path, content):
    with open(file_path, "+w") as file:

        file.write(content)
