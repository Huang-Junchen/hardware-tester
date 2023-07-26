import os
import time
import argparse
from datetime import datetime
from utils.CpuTester import CpuTester
from utils.GpuTester import GpuTester


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu-only', help='Only record CPU temperature', action='store_true')
    parser.add_argument('--sample-interval',
                        help='Specify the data retrieve interval in seconds. Default is 10 seconds',
                        type=int, default=10)
    parser.add_argument('--log-file', help='Record CSV file. Default is ./statistic.csv',
                        type=str, default='./statistic.csv')
    return parser.parse_args()


def write_record_file(file_handle, content):
    file_handle.write(content + '\n')
    print("[DEBUG] " + content + '\n')


def generate_table_header(cpu_num, gpu_num=0):
    cpu_header = ','.join(["cpu" + str(i) + "_temp,cpu" + str(i) + "_util" for i in range(cpu_num)])
    gpu_header = ','.join(["gpu" + str(i) + "_util,gpu" + str(i) + "_mem_util,gpu" + str(i) + "_temp,gpu" + str(
        i) + "_pw_usage,gpu" + str(i) + "_graphics_freq,gpu" + str(i) + "_sm_greq,gpu" + str(i) + "_mem_freq,gpu" + str(
        i) + "_video_freq" for i in range(gpu_num)])
    return 'datetime,' + cpu_header + ',' + gpu_header


def open_log_handle(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    return open(file_path, 'a')


def main():
    args = get_args()
    sample_interval = args.sample_interval

    log_file = args.log_file
    log_file_handle = open_log_handle(log_file)

    cpu_tester = None
    gpu_tester = None

    print()
    try:
        if not args.cpu_only:
            print("[INFO] Start to record GPU/CPU temperature in every {} sec.".format(str(sample_interval)))
            cpu_tester = CpuTester()
            gpu_tester = GpuTester()
            write_record_file(log_file_handle, generate_table_header(cpu_tester.num, gpu_tester.num))
        else:
            print("[WARN] Only collect CPU Temperature.")
            print("[INFO] Start to record CPU temperature in every {} sec.".format(str(sample_interval)))
            cpu_tester = CpuTester()
            write_record_file(log_file_handle, generate_table_header(cpu_tester.num))

        while True:
            timestamp = str(datetime.now()).split('.')[0]
            data_row = [timestamp]
            data_row.extend(cpu_tester.get_statistics())
            if gpu_tester is not None:
                data_row.extend(gpu_tester.get_statistics())

            write_record_file(log_file_handle, ','.join(data_row))
            time.sleep(sample_interval)

    except KeyboardInterrupt:
        print()
        print("[ERROR] Keyboard Interrupted, temperature recording program exit.")
        exit()


if __name__ == '__main__':
    main()
