from os.path import abspath, join, dirname, isfile

MAIN_PATH = dirname(__file__)
DYNAMIC_LOG_PATH = join(MAIN_PATH, 'Logs','dynamic_log.txt')
LOG_PATH = join(MAIN_PATH, 'Logs','log.txt')

class LogManager(object):

    def create_logs(self):
        self.write_log(log_path=LOG_PATH, text_to_write='')
        self.write_log(log_path=DYNAMIC_LOG_PATH, text_to_write='')
        return True

    def append_to_all_logs(self, text_text_append):
        self.append_to_log(log_path=LOG_PATH, text_to_append=text_text_append)
        self.append_to_log(log_path=DYNAMIC_LOG_PATH, text_to_append=text_text_append)

    def read_log(self, log_path):
        with open(log_path, 'r') as log:
            log_text = log.read()
        return log_text

    def read_lines(self, log_path):
        with open(log_path, 'r') as log:
            log_text = log.readlines()
        return log_text

    def read_first_line_and_erase(self, log_path=DYNAMIC_LOG_PATH):
        log_text_lines = self.read_lines(log_path=log_path)

        if len(log_text_lines) > 0:
            wanted_content = log_text_lines[0]
            string_to_write_back = ''.join(log_text_lines[1:])
            self.write_log(log_path=log_path, text_to_write=string_to_write_back)
            return wanted_content
        else:
            return None


    def write_log(self, log_path, text_to_write):
        with open(log_path, 'w') as log:
            log.write(text_to_write)
        return True

    def append_to_log(self, log_path, text_to_append):
        with open(log_path, 'r') as log:
            log_text = log.read()
        log_text = '\n'.join([log_text, text_to_append])
        return self.write_log(log_path=log_path, text_to_write=log_text)

    def erase_log(self, log_path):
        return self.write_log(log_path=log_path, text_to_write='')
