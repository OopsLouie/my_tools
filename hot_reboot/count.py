#! /usr/bin/python3
success = 0
fail = 0
with open("/lspci_res","r") as f:
    for i in f.readlines():
        if i == "success\n":
            success += 1
        else:
            fail +=  1
print("success count is {0}".format(success))
print("fail count is {0}".format(fail))

