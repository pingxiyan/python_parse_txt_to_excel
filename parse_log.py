import sys
import os.path as p
import argparse

# Parse log
def parse(input_name):
    print("==========================================")
    print("Start parse...")
    # Using readlines()
    file1 = open(input_name, 'r')
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