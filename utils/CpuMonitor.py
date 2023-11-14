import subprocess
import psutil
from utils.Printer import print_info


class CpuMonitor:
    def __init__(self):
        self.num = self.get_num()

        self.print_info()

    @staticmethod
    def get_info():
        """
        使用sensors获取cpu信息
        :return: cpu info
        """
        cmd = [['sensors'], ['grep', '-i', '-E', "(physical|package) id"], ['sort']]
        sensors_output = subprocess.Popen(cmd[0], stdout=subprocess.PIPE)
        sort_output = subprocess.Popen(cmd[1], stdin=sensors_output.stdout, stdout=subprocess.PIPE)
        output = subprocess.check_output(cmd[2], stdin=sort_output.stdout)
        sensors_output.wait()
        sort_output.wait()
        output = [line for line in output.split(b'\n') if line.strip() != b""]
        return output

    def get_num(self):
        """
        获取cpu个数
        :return: cpu number
        """
        return len(self.get_info())

    def get_util(self):
        """
        使用psutil 获得cpu的使用率
        :return: cpu util
        """
        util_list = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_util_list = [sum(util_list[len(util_list) // self.num * i: (i + 1) * len(util_list) // self.num]) // (
                len(util_list) // self.num) for i in range(self.num)]
        return cpu_util_list

    def get_temperature(self):
        """
        使用cpu info 解析获得cpu温度
        :return: cpu temperature
        """
        cpu_temp_list = []
        raw_output = self.get_info()
        for line in raw_output:
            cpu_temp_list.append(line.split(b'+')[1].split(b'\xc2\xb0C')[0].decode())
        return cpu_temp_list

    def get_statistics(self):
        """
        获取单个或多个 cpu 的温度和使用率的统计信息
        :return: cpu temperature & util list
        """
        statistics = []
        cpu_util_statistics = self.get_util()
        cpu_temp_statistics = self.get_temperature()
        for cpu_statistic in zip(cpu_temp_statistics, cpu_util_statistics):
            statistics.append(str(cpu_statistic[0]))
            statistics.append(str(round(cpu_statistic[1], 2)))

        return statistics

    def print_info(self):
        print_info("[INFO] CPU Numbers: {}".format(str(self.num)))
