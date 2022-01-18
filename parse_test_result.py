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
    
    TotalDemos = len(AllRslt)
    TotalErrDemosNum = 0
    TotalCases = 0
    TotalErrCasesNum = 0
    # Statistic
    for r in AllRslt:
        if r["err_num"] != 0:
            TotalErrDemosNum += 1
        TotalCases += r["demo_num"]
        TotalErrCasesNum += r["err_num"]
        # print("  {}: {}/{}".format(r["demo"], r["err_num"], r["demo_num"]))

    # Workbook is created
    wb = Workbook()
    # Specifying style: font: bold on, height 320
    style_title = xlwt.easyxf('font: bold on, height 280; pattern: pattern solid, fore_colour blue;')
    # pattern: pattern solid, fore_colour light_blue;
    style_left = xlwt.easyxf('align: horiz left;')
    style_center = xlwt.easyxf('align: horiz center;')
    style_yellow = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
    style_center_yellow = xlwt.easyxf('align: horiz center; pattern: pattern solid, fore_colour yellow;') # light_yellow
    style_center_red = xlwt.easyxf('align: horiz center; pattern: pattern solid, fore_colour red;') 
    # Applying multiple styles
    style2 = xlwt.easyxf('font: bold 1, color red;')

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Summary', cell_overwrite_ok=True)
    sheet1.col(0).width = 256 * 50  # 50 characters wide (-ish)
    sheet1.col(2).width = 256 * 16
    sheet1.col(3).width = 256 * 16
    sheet1.col(4).width = 256 * 16
    sheet1.col(5).width = 256 * 16
    sheet1.col(6).width = 256 * 50

    row = 1
    for i in range(10): sheet1.write(row, i, "", style_title)
    sheet1.write(row, 0, 'OMZ version')
    row += 1

    for i in range(10): sheet1.write(row, i, "", style_title)
    sheet1.write(row, 0, 'OpenVINO version', style_title)
    row += 2
    
    for i in range(10): sheet1.write(row, i, "", style_title)
    sheet1.write(row, 0, 'Result Summary', style_title); sheet1.write(row, 1, 'Total', style_title)
    row += 1
    sheet1.write(row, 0, 'Passed Demos');  sheet1.write(row, 1, TotalDemos, style_center); 
    row += 1
    sheet1.write(row, 0, 'Failed Demos');  sheet1.write(row, 1, TotalErrDemosNum, style_center); 
    row += 1
    sheet1.write(row, 0, 'Passed Cases');  sheet1.write(row, 1, TotalCases - TotalErrCasesNum, style_center); 
    row += 1
    sheet1.write(row, 0, 'Failed Cases');  sheet1.write(row, 1, TotalErrCasesNum, style_center); 
    row += 2

    # Diagram

    # Detials
    for i in range(10): sheet1.write(row, i, "", style_title)
    sheet1.write(row, 0, 'Demo Name', style_title)
    sheet1.write(row, 4, 'AUTO:CPU,GPU', style_title); sheet1.write(row, 5, 'MULTI:CPU,GPU', style_title); sheet1.write(row, 6, 'COMMENT', style_title)
    row += 1
    for r in AllRslt:
        cur_style = style_left
        cur_styles = style_center
        if r["err_num"] != 0:
            cur_style = style_yellow
            cur_styles = style_center_yellow
        
        sheet1.write(row, 0, r["demo"], cur_style)
        sheet1.write(row, 1, "", cur_styles)
        sheet1.write(row, 2, "", cur_styles)
        sheet1.write(row, 3, "", cur_styles)
        sheet1.write(row, 4, "{}/{}".format(r["demo_num"] - r["err_num"], r["demo_num"]), cur_styles)
        sheet1.write(row, 5, "", cur_styles)
        sheet1.write(row, 6, "", cur_styles)
        row += 1

    print("Test_Demos_Num: {}, {}/{}".format(TotalDemos, TotalErrCasesNum, TotalCases))
    
    global g_output_name
    wb.save(g_output_name)

if __name__ == "__main__":
   parse_param()
   rslt = parse_log()
   export_excel(rslt)
