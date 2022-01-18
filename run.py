import sys
import os.path as p
import argparse
import save_xls
import save_xlsx
from parse_log import parse

g_input_name = ""
g_output_name = ""

def parse_param():
    parser = argparse.ArgumentParser(description='Parse input parameters.')
    parser.add_argument('-i', default = "run_test_log_gpu_1.log",
                        help='Input log file.')
    parser.add_argument('-o', default="output.xls",
                        help='Output excel report')
    args = parser.parse_args()

    global g_input_name
    global g_output_name
    g_input_name = args.i
    g_output_name = args.o
    print("g_input_name=", g_input_name)
    print("g_output_name=", g_output_name)

if __name__ == "__main__":
    parse_param()
    rslt = parse(g_input_name)
    save_xls.export_excel_xls(rslt, g_output_name)
    # save_xlsx.export_excel_xlsx(rslt, g_output_name)
