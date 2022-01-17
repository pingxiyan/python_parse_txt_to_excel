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
    parser.add_argument('-o', default="output.xlsx",
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

    Test_Coms_Num = 0

    Test_One_Com_Num = 0
    Test_One_Com_Err_Num = 0
    Test_One_Com_Err_LOGS = []

    FlagProcessComs = 0
    AllComs = []
    G_OldComName = ""

    # Parse
    count = 0
    for line in Lines:
        count += 1

        # Compare each line flag.
        if FlagProcessComs == 1:
            if line[0:11] == "Test case #":
                Test_One_Com_Num += 1
                print("  #{}".format(line[0:13]))
            elif line[0:10] == "Exit code:":
                Test_One_Com_Err_Num += 1
            elif line[0:9] == "No exist:":
                Test_One_Com_Err_Num += 1
        
        # Find one Component:
        if line[0:8] == "Testing ":
            if FlagProcessComs == 1:
                AllComs.append({"com": G_OldComName, "case_num": Test_One_Com_Num, "err_num":Test_One_Com_Err_Num})
                Test_One_Com_Num = 0
                Test_One_Com_Err_Num = 0

            G_OldComName=line[8:-4]
            print("Com: {}, ".format(G_OldComName))

            Test_Coms_Num += 1
            FlagProcessComs = 1
            continue

    # Append last component.
    if FlagProcessComs == 1:
        AllComs.append({"com": G_OldComName, "case_num": Test_One_Com_Num, "err_num":Test_One_Com_Err_Num})
        Test_One_Com_Num = 0
        Test_One_Com_Err_Num = 0

    print("Test_Coms_Num: {}".format(Test_Coms_Num))
    for c in AllComs:
        print("  {}: {}/{}".format(c["com"], c["err_num"], c["case_num"]))

    print("parse_log done.")
    return AllComs

def export_excel(AllRslt):
    print("========================")
    print("Start export to excel...")
    
    TotalComs = len(AllRslt)
    TotalCases = 0
    TotalErrNum = 0
    for r in AllRslt:
       TotalCases += r["case_num"]
       TotalErrNum += r["err_num"]
       print("  {}: {}/{}".format(r["com"], r["err_num"], r["case_num"]))
    
    print("Test_Coms_Num: {}, {}/{}".format(TotalComs, TotalErrNum, TotalCases))
  
    # Workbook is created
    wb = Workbook()
    
    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    
    sheet1.write(1, 0, 'ISBT DEHRADUN')
    sheet1.write(2, 0, 'SHASTRADHARA')
    sheet1.write(3, 0, 'CLEMEN TOWN')
    sheet1.write(4, 0, 'RAJPUR ROAD')
    sheet1.write(5, 0, 'CLOCK TOWER')
    sheet1.write(0, 1, 'ISBT DEHRADUN')
    sheet1.write(0, 2, 'SHASTRADHARA')
    sheet1.write(0, 3, 'CLEMEN TOWN')
    sheet1.write(0, 4, 'RAJPUR ROAD')
    sheet1.write(0, 5, 'CLOCK TOWER')
    
    global g_output_name
    wb.save(g_output_name)

if __name__ == "__main__":
   parse_param()
   rslt = parse_log()
   export_excel(rslt)
