import sys
import os.path as p
import argparse
# importing xlwt module
import xlwt
from xlwt import Workbook

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

def parse_log():
    global g_input_name
    global g_output_name

    print("========================")
    print("Start parse...")
    # Using readlines()
    file1 = open(g_input_name, 'r')
    Lines = file1.readlines()

    Test_Demos_Num = 0

    Test_One_Demo_Num = 0
    Test_One_Demo_Err_Num = 0

    FlagProcessDemos = 0
    AllDemos = []
    G_OldDemoName = ""

    # Parse
    count = 0
    for line in Lines:
        count += 1

        # Compare each line flag.
        if FlagProcessDemos == 1:
            if line[0:11] == "Test case #":
                Test_One_Demo_Num += 1
                print("  #{}".format(line[0:13]))
            elif line[0:10] == "Exit code:":
                Test_One_Demo_Err_Num += 1
            elif line[0:9] == "No exist:":
                Test_One_Demo_Err_Num += 1
        
        # Find one Component:
        if line[0:8] == "Testing ":
            if FlagProcessDemos == 1:
                AllDemos.append({"demo": G_OldDemoName, "demo_num": Test_One_Demo_Num, "err_num":Test_One_Demo_Err_Num})
                Test_One_Demo_Num = 0
                Test_One_Demo_Err_Num = 0

            G_OldDemoName=line[8:-4]
            print("Com: {}, ".format(G_OldDemoName))

            Test_Demos_Num += 1
            FlagProcessDemos = 1
            continue

    # Append last component.
    if FlagProcessDemos == 1:
        AllDemos.append({"demo": G_OldDemoName, "demo_num": Test_One_Demo_Num, "err_num":Test_One_Demo_Err_Num})
        Test_One_Demo_Num = 0
        Test_One_Demo_Err_Num = 0

    print("Test_Demos_Num: {}".format(Test_Demos_Num))
    for c in AllDemos:
        print("  {}: {}/{}".format(c["demo"], c["err_num"], c["demo_num"]))

    print("parse_log done.")
    return AllDemos

def export_excel(AllRslt):
    print("========================")
    print("Start export to excel...")
    
    TotalComs = len(AllRslt)
    TotalErrComNum = 0
    TotalCases = 0
    TotalErrNum = 0
    # Statistic
    for r in AllRslt:
       TotalCases += r["demo_num"]
       TotalErrNum += r["err_num"]
    #    print("  {}: {}/{}".format(r["demo"], r["err_num"], r["demo_num"]))

    # Workbook is created
    wb = Workbook()
    # Specifying style: font: bold on, height 320
    style1 = xlwt.easyxf('font: bold on')
    # Applying multiple styles
    style2 = xlwt.easyxf('font: bold 1, color red;')

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Summary')
    
    row = 1
    sheet1.write(row, 0, 'OMZ version', style1)
    row += 1

    sheet1.write(row, 0, 'OpenVINO version', style1)
    row += 2
    
    sheet1.write(row, 0, 'Result Summary', style1); sheet1.write(row, 1, 'Total', style1)
    row += 1
    sheet1.write(row, 0, 'Passed Demos');  sheet1.write(row, 1, TotalComs); 
    row += 1
    sheet1.write(row, 0, 'Failed Demos');  sheet1.write(row, 1, TotalComs); 
    row += 1
    sheet1.write(row, 0, 'Passed Cases');  sheet1.write(row, 1, TotalCases - TotalErrNum); 
    row += 1
    sheet1.write(row, 0, 'Failed Cases');  sheet1.write(row, 1, TotalErrNum); 
    row += 2

    # Diagram

    # Detials
    sheet1.write(row, 0, 'Demo Name', style1)
    sheet1.write(row, 4, 'AUTO:CPU,GPU', style1); sheet1.write(row, 5, 'MULTI:CPU,GPU', style1); sheet1.write(row, 6, 'COMMENT', style1)
    row += 1
    for r in AllRslt:
       sheet1.write(row, 0, r["demo"])
       sheet1.write(row, 4, "{}/{}".format(r["err_num"], r["demo_num"]))
       row += 1

    print("Test_Demos_Num: {}, {}/{}".format(TotalComs, TotalErrNum, TotalCases))
    
    global g_output_name
    wb.save(g_output_name)

if __name__ == "__main__":
   parse_param()
   rslt = parse_log()
   export_excel(rslt)
