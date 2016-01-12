from os.path import abspath, join, dirname, isfile

MAIN_PATH = dirname(__file__)
GEAR_DYNAMIC_LOG_PATH = join(MAIN_PATH, 'Logs','gear_dynamic_log.txt')
GEAR_LOG_PATH = join(MAIN_PATH, 'Logs','gear_log.txt')

BREAK_DYNAMIC_LOG_PATH = join(MAIN_PATH, 'Logs','break_dynamic_log.txt')
BREAK_LOG_PATH = join(MAIN_PATH, 'Logs','break_log.txt')

class LogManager(object):

    def get_correct_logs(self, case):

        if case == 'gear':
            dynamic_log_path = GEAR_DYNAMIC_LOG_PATH
            log_path = GEAR_LOG_PATH

        else:
            dynamic_log_path = BREAK_DYNAMIC_LOG_PATH
            log_path = BREAK_LOG_PATH

        return log_path, dynamic_log_path

    def create_logs(self):

        # Break Case
        self.write_log(log_path=BREAK_LOG_PATH, text_to_write='')
        self.write_log(log_path=BREAK_DYNAMIC_LOG_PATH, text_to_write='')

        # Gear Case
        self.write_log(log_path=GEAR_LOG_PATH, text_to_write='')
        self.write_log(log_path=GEAR_DYNAMIC_LOG_PATH, text_to_write='')
        return True

    def finish_logs(self):

        # Break Case
        self.write_log(log_path=BREAK_DYNAMIC_LOG_PATH, text_to_write='finished')

        # Gear Case
        self.write_log(log_path=GEAR_DYNAMIC_LOG_PATH, text_to_write='finished')
        return True

    def append_to_all_logs(self, text_text_append, case):

        log_path, dynamic_log_path = self.get_correct_logs(case=case)

        self.append_to_log(log_path=log_path, text_to_append=text_text_append)
        self.append_to_log(log_path=dynamic_log_path, text_to_append=text_text_append)

    def read_log(self, log_path):
        with open(log_path, 'r') as log:
            log_text = log.read()
        return log_text

    def read_lines(self, log_path):
        with open(log_path, 'r') as log:
            log_text = log.readlines()
        return log_text

    def read_first_line_and_erase(self, case):

        log_path, dynamic_log_path = self.get_correct_logs(case=case)

        log_text_lines = self.read_lines(log_path=dynamic_log_path)

        if len(log_text_lines) > 0:
            wanted_content = log_text_lines[0]
            string_to_write_back = ''.join(log_text_lines[1:])
            self.write_log(log_path=dynamic_log_path, text_to_write=string_to_write_back)
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
