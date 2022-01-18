import sys
import os.path as p
# importing xlwt module
import xlwt
from xlwt import Workbook

def set_one_row_style(sheet, row, style):
    for i in range(17):
        sheet.write(row, i, "", style)

def export_excel_xls(AllRslt, output_name):
    print("========================")
    print("Start export to excel...")
    
    TotalDemos = len(AllRslt)
    TotalPassDemosNum = 0
    TotalErrDemosNum = 0
    TotalCases = 0
    TotalPassCasesNum = 0
    TotalErrCasesNum = 0
    # Statistic
    for r in AllRslt:
        if r["err_num"] != 0:
            TotalErrDemosNum += 1
        TotalCases += r["demo_num"]
        TotalErrCasesNum += r["err_num"]
        # print("  {}: {}/{}".format(r["demo"], r["err_num"], r["demo_num"]))

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
    sheet1.col(2).width = 256 * 24
    sheet1.col(3).width = 256 * 24
    sheet1.col(4).width = 256 * 24
    sheet1.col(5).width = 256 * 24
    sheet1.col(6).width = 256 * 50

    row = 1
    set_one_row_style(sheet1, row, style_title)
    sheet1.write(row, 0, 'OMZ version', style_title)
    row += 1

    set_one_row_style(sheet1, row, style_title)
    sheet1.write(row, 0, 'OpenVINO version', style_title)
    row += 2
    
    set_one_row_style(sheet1, row, style_title)
    sheet1.write(row, 0, 'Result Summary', style_title); sheet1.write(row, 1, 'Total', style_title)
    row += 1
    sheet1.write(row, 0, 'Total Demos');  sheet1.write(row, 1, TotalDemos, style_center_yellow); 
    row += 1
    sheet1.write(row, 0, 'Passed Demos');  sheet1.write(row, 1, TotalDemos - TotalErrDemosNum, style_center); 
    row += 1
    sheet1.write(row, 0, 'Failed Demos');  sheet1.write(row, 1, TotalErrDemosNum, style_center); 
    row += 1

    sheet1.write(row, 0, 'Total Cases');  sheet1.write(row, 1, TotalCases, style_center_yellow); 
    row += 1
    sheet1.write(row, 0, 'Passed Cases');  sheet1.write(row, 1, TotalCases - TotalErrCasesNum, style_center); 
    row += 1
    sheet1.write(row, 0, 'Failed Cases');  sheet1.write(row, 1, TotalErrCasesNum, style_center); 
    row += 2

    # Diagram
    # ============================================================
    # Create a new Chart object.

    # Detials
    # ============================================================
    set_one_row_style(sheet1, row, style_title)
    sheet1.write(row, 0, 'Demo Name', style_title)
    sheet1.write(row, 4, 'AUTO:CPU,GPU', style_title); sheet1.write(row, 5, 'MULTI:CPU,GPU', style_title); sheet1.write(row, 6, 'COMMENT', style_title)
    row += 1
    for r in AllRslt:
        cur_style = style_left
        cur_styles = style_center
        if r["err_num"] != 0:
            cur_style = style_yellow
            cur_styles = style_center_yellow
            set_one_row_style(sheet1, row, style_yellow)
        
        sheet1.write(row, 0, r["demo"], cur_style)
        sheet1.write(row, 1, "", cur_styles)
        sheet1.write(row, 2, "", cur_styles)
        sheet1.write(row, 3, "", cur_styles)
        sheet1.write(row, 4, "{}/{}".format(r["demo_num"] - r["err_num"], r["demo_num"]), cur_styles)
        sheet1.write(row, 5, "", cur_styles)
        sheet1.write(row, 6, "", cur_styles)
        row += 1

    print("Test_Demos_Num: {}, {}/{}".format(TotalDemos, TotalErrCasesNum, TotalCases))
    wb.save(output_name)