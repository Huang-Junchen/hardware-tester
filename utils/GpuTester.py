import pynvml


class GpuTester:
    def __init__(self):
        self.init_driver()

        self.num = self.get_num()
        self.drive_version = self.get_driver_ver()
        self.handles = self.get_handles()

        self.print_info()

    @staticmethod
    def init_driver():
        """
        初始化驱动包
        :return:
        """
        try:
            pynvml.nvmlInit()
            print("[INFO] pynvml Initialized.")
        except Exception:
            print(
                "[ERROR] NVML driver initialize failed. Maybe there is no GPU in this system or the GPU driver is not installed properly!")

    @staticmethod
    def get_num():
        """
        获得gpu数量
        :return: gpu num
        """
        return int(pynvml.nvmlDeviceGetCount())

    @staticmethod
    def get_driver_ver():
        """
        获取gpu驱动版本
        :return: gpu driver version
        """
        return pynvml.nvmlSystemGetDriverVersion()

    def get_handles(self):
        """
        获取gpu处理句柄
        :return: gpu handles
        """
        gpu_handles = [pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(self.num)]
        # print("[DEBUG] GPU Handles: {}".format(gpu_handles))

        return gpu_handles

    def get_statistics(self):
        """
        获取单个或多个 gpu 的温度和使用率的统计信息
        :return: statistics list
        """
        statistics = []
        statistic = []
        for gpu in self.handles:
            temp = pynvml.nvmlDeviceGetTemperature(gpu, pynvml.NVML_TEMPERATURE_GPU)
            utils = str(pynvml.nvmlDeviceGetUtilizationRates(gpu)).split()
            mem_utils = str(pynvml.nvmlDeviceGetMemoryInfo(gpu)).split()
            mem_usage_rate = round(float(mem_utils[7]) / float(mem_utils[1]) * 100, 2)
            pw_usage = str(pynvml.nvmlDeviceGetPowerUsage(gpu))
            pw_usage = pw_usage[:-3] + "." + pw_usage[-3:]
            freq_graphic = str(pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_GRAPHICS))
            freq_sm = str(pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_SM))
            freq_mem = str(pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_MEM))
            freq_video = str(pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_VIDEO))
            statistics.append(
                {'temperature': temp, 'gpu_util': utils[1], 'gpu_mem_util': mem_usage_rate, 'pw_usage': pw_usage,
                 'freq_graphic': freq_graphic, 'freq_sm': freq_sm, 'freq_mem': freq_mem,
                 'freq_video': freq_video})

        for statistics in statistics:
            statistic.append(str(statistics['gpu_util']))
            statistic.append(str(statistics['gpu_mem_util']))
            statistic.append(str(statistics['temperature']))
            statistic.append(str(statistics['pw_usage']))
            statistic.append(str(statistics['freq_graphic']))
            statistic.append(str(statistics['freq_sm']))
            statistic.append(str(statistics['freq_mem']))
            statistic.append(str(statistics['freq_video']))

        return statistic

    def print_info(self):
        print("[INFO] Driver version: {}".format(self.drive_version))

        print("[INFO] GPU Numbers: {}".format(str(self.num)))

        print()



