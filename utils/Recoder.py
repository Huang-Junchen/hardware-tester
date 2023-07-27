import os
from utils.Printer import print_info


class Recoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.handle = self.get_handle()
        self.print_info()
        pass

    def get_handle(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        return open(self.file_path, 'a')

    @staticmethod
    def generate_table_header(cpu_num, gpu_num=0):
        cpu_header = ','.join(["cpu" + str(i) + "_temp,cpu" + str(i) + "_util" for i in range(cpu_num)])
        gpu_header = ','.join(["gpu" + str(i) + "_util,gpu" + str(i) + "_mem_util,gpu" + str(i) + "_temp,gpu" + str(
            i) + "_pw_usage,gpu" + str(i) + "_graphics_freq,gpu" + str(i) + "_sm_greq,gpu" + str(
            i) + "_mem_freq,gpu" + str(
            i) + "_video_freq" for i in range(gpu_num)])
        header = 'datetime,' + cpu_header + ',' + gpu_header
        print(header)
        return header

    def write_record_file(self, content):
        self.handle.write(content + '\n')
        print("[DEBUG] " + content + '\n')

    def print_info(self):
        print_info("[INFO] Log File Path: {}".format(str(self.file_path)))


