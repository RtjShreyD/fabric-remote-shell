# import ghlinguist as ghl

# langs = ghl.linguist('~/TecE/TE-web/te-web-aws')

# print(langs)

import subprocess
try:
    # test = subprocess.Popen(["github-linguist"], stdout=subprocess.PIPE, cwd = '/home/rtj/TecE/TE-web/te-web-aws')
    test2 = subprocess.Popen(["sudo apt update"], stdout=subprocess.PIPE)
    #output = test.communicate()[0]
    output2 = test2.communicate()
    
except:
    # output = "Error"
    output2 = "Error"

# print(output)
print(output2)