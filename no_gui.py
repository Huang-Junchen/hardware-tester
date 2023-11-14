import os
import time
import argparse
from datetime import datetime
from utils.CpuMonitor import CpuMonitor
from utils.GpuMonitor import GpuMonitor
from utils.Recoder import Recoder
from utils.Printer import print_info, print_err, print_warn


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu-only', help='Only record CPU temperature', action='store_true')
    parser.add_argument('--sample-interval',
                        help='Specify the data retrieve interval in seconds. Default is 10 seconds',
                        type=int, default=10)
    parser.add_argument('--log-file', help='Record CSV file. Default is ./statistic.csv',
                        type=str, default='./statistic.csv')
    return parser.parse_args()


def main():
    args = get_args()
    sample_interval = args.sample_interval

    log_file = args.log_file
    log = Recoder(log_file)

    cpu_tester = None
    gpu_tester = None

    try:
        if not args.cpu_only:
            print_info("[INFO] Start to record GPU/CPU temperature in every {} sec.".format(str(sample_interval)))
            cpu_tester = CpuMonitor()
            gpu_tester = GpuMonitor()
            log.generate_table_header(cpu_tester.num, gpu_tester.num)
        else:
            print_warn("[WARN] Only collect CPU Temperature.")
            print_info("[INFO] Start to record CPU temperature in every {} sec.\033[0m".format(str(sample_interval)))
            cpu_tester = CpuMonitor()
            log.generate_table_header(cpu_tester.num)

        while True:
            timestamp = str(datetime.now()).split('.')[0]
            data_row = [timestamp]
            data_row.extend(cpu_tester.get_statistics())
            if gpu_tester is not None:
                data_row.extend(gpu_tester.get_statistics())

            log.write_record_file(','.join(data_row))
            time.sleep(sample_interval)

    except KeyboardInterrupt:
        print()
        print_err("[ERROR] Keyboard Interrupted, temperature recording program exit.")
        exit()


if __name__ == '__main__':
    main()
