import os
import subprocess
from os.path import dirname, abspath, join


class GpuStressTester:
    def __init__(self):
        self.process = None

    def start_test(self, duration, gpu_index=None):
        if self.process is not None and self.process.poll() is None:
            print("A GPU stress test is already running.")
            return

        # 获取当前脚本所在的目录
        current_script_dir = dirname(abspath(__file__))
        # 假设 gpu-burn 目录在当前脚本所在目录的上一级目录中
        gpu_burn_path = join(current_script_dir, '..', 'gpu-burn')

        os.chdir(gpu_burn_path)  # 切换到 GPU Burn 的目录
        command = ["./gpu_burn", str(duration)]

        if gpu_index is not None:
            command.insert(0, f'CUDA_VISIBLE_DEVICES={gpu_index}')

        try:
            self.process = subprocess.Popen(command)
        except Exception as e:
            print(f"Failed to start GPU stress test: {e}")

    def stop_test(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            print("\nGPU stress test stopped.")
        else:
            print("\nNo GPU stress test is running.")

# 使用示例
# gpu_tester = GpuStressTester()
# gpu_tester.start_test(60)  # 运行60秒的GPU压力测试
# gpu_tester.stop_test()     # 停止测试
