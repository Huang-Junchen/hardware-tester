import subprocess


class CpuStressTester:
    def __init__(self):
        self.process = None
        self.core_num = self.get_core_num()
        pass

    def start_test(self, core_number, duration):
        if self.process is not None and self.process.poll() is None:
            print("A stress test is already running.")
            return

        command = ["stress", "-c", str(core_number), "-t", str(duration)]
        try:
            self.process = subprocess.Popen(command)
        except Exception as e:
            print(f"Failed to start stress test: {str(e)}")

    def stop_test(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("CPU stress test stopped.")
        else:
            print("No CPU stress test is running.")


    def get_core_num(self):
        """
        获取cpu总核心数
        :return: cpu core number
        """
        cmd = [['sensors'], ['grep', '-i', '-E', "Core "], ['sort']]
        sensors_output = subprocess.Popen(cmd[0], stdout=subprocess.PIPE)
        sort_output = subprocess.Popen(cmd[1], stdin=sensors_output.stdout, stdout=subprocess.PIPE)
        output = subprocess.check_output(cmd[2], stdin=sort_output.stdout)
        sensors_output.wait()
        sort_output.wait()
        output = [line for line in output.split(b'\n') if line.strip() != b""]
        return len(output)




