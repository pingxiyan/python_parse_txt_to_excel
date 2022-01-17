import os.path as p

# Using readlines()
file1 = open('run_tests2_ww0303.log', 'r')
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

    if FlagProcessComs == 1:
        if line[0:11] == "Test case #":
            Test_One_Com_Num += 1
            print("  #{}".format(line[0:13]))
        if line[0:10] == "Exit code:":
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
