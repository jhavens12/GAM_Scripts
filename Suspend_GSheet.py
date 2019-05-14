import pygsheets
from pprint import pprint
import os
import sys

#Works with google sheets instead of a copy/paste text file like previous verisons
gc = pygsheets.authorize()

# Open spreadsheet and then workseet
sh = gc.open('18/19 Student List')
wks = sh.worksheet_by_title("Suspend")

#####
exclude_header = True
#####

if exclude_header:
    row = 2
else:
    row = 1

column = 7 #username
val_1 = wks.get_values(start=(row,column), end=(9999,column), returnas='matrix') #8 is how many over

for id in val_1:
    print(id[0])
    #gam_input = "~/bin/gam/gam update user "+id[0]+" org '/Students/GY"+str(year[0])+"'"
    gam_input = "~/bin/gam/gam update user "+id[0]+" suspended on"
    result_1 = os.popen(gam_input).read()
    print(result_1)
