import os
import sys
from itertools import islice

grade_book = {'12': 19, '11': 20, '10': 21, '9': 22, '8': 23,'7': 24, \
    '6': 25, '5': 26, '4': 27, '3':28, '2':29, '1':30}

def query_yes_no(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        #choice = choice.strip()
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

print("Milton v1.1 5/14/19")
print("Starting...")
result_test = os.popen("~/bin/gam/gam info user jhavens").read()

question_1 = "Do you wish to create NEW USER?"
choice_1 = query_yes_no(question_1, default="yes")
if choice_1:

    question_2 = "Is this a Staff Member?"
    choice_2 = query_yes_no(question_2, default="yes")
    if choice_2:

        first_name = input('First Name: ')
        last_name = input('Last Name: ')

        #NEWFIRST_I_L = first_name[0].lower()
        #NEWLAST_I_L = last_name[0].lower()
        NEWUSER = first_name[0].lower() + last_name.lower()
        NEWEMAIL = NEWUSER + "@mymtsd-vt.org"
        NEWDEFAULTPW = first_name[0].lower() + last_name.lower() + "123"
        gam_input = "~/bin/gam/gam create user "+NEWUSER+" firstname "+first_name+" lastname "+last_name+" password "+NEWDEFAULTPW+" changepassword off org '/Faculty_Staff'"
        #print(gam_input)
        result_1 = os.popen(gam_input).read()
        print(result_1)

    if not choice_2:
        question_3 = "Is this a Student?"
        choice_3 = query_yes_no(question_3, default="yes")
        if choice_3:

            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            grade = input('Grade: ')
            grad_year = grade_book[grade]

            #NEWFIRST_I_L = first_name[:3].lower()
            #NEWLAST_I_L = last_name[0].lower()
            NEWUSER = first_name[:3].lower() + last_name.lower()
            NEWEMAIL = NEWUSER + "@mymtsd-vt.org"
            NEWDEFAULTPW = first_name[:3].lower() + last_name.lower() + "123"
            gam_input = "~/bin/gam/gam create user "+NEWUSER+" firstname "+first_name+" lastname "+last_name+" password "+NEWDEFAULTPW+" changepassword off org '/Students/GY20"+str(grad_year)+"'"
            #print(gam_input)
            result_1 = os.popen(gam_input).read()
            print(result_1)

    print()
    print("Newly Created User Info:")
    print("Name: "+first_name+" "+last_name)
    print("User: "+NEWUSER)
    print("Email: "+NEWEMAIL)
    print("Password: "+NEWDEFAULTPW)
    print()

    gam_input = "~/bin/gam/gam info user "+NEWUSER
    result_1 = os.popen(gam_input).read()
    print(result_1)
    print()

##########################################################
##########################################################
##########################################################

question = "Do you wish to modify EXISTING USER?"
choice = query_yes_no(question, default="yes")
if choice:
    existing_user_name = input('Username? (just user - no email) ')
    existing_email = existing_user_name + "@mymtsd-vt.org"
    print("Info:")
    print()
    gam_input = "~/bin/gam/gam info user "+existing_user_name
    result_1 = os.popen(gam_input).read()
    result_2 = result_1
    head = list(islice(result_1.splitlines(), 19))
    for x in head:
        print(x)

    ## Groups
    group_list= []
    group_dictionary= {}
    for x in result_1.splitlines():
        if "@" in x and "User" not in x and existing_user_name not in x: #filter out results that aren't actual groups
            a = x.split('<',1)[-1]
            b = a.replace(">", "")
            group_list.append(b)

    for x in group_list:
        gam_input = "~/bin/gam/gam info group "+x
        result_1 = os.popen(gam_input).read()
        for y in result_1.splitlines():
            if existing_email in y:
                w = y.split(':',1)[0].strip()
                group_dictionary[x] = w
    print()
    print("Groups:")
    for x in group_dictionary:

        print(group_dictionary[x], x)

    #variable creation
    for x in result_2.splitlines():
        if "First Name:" in x:
            first_name = x.split(':',1)[-1].strip()
        if "Last Name:" in x:
            last_name = x.split(':',1)[-1].strip()
        if "Must Change Password:" in x:
            PW_Flag = x.split(':',1)[-1].strip()
        if "Account Suspended:" in x:
            account_suspended = x.split(':',1)[-1].strip()
    #NEWFIRST_I_L = first_name[0].lower()
    #NEWLAST_I_L = last_name[0].lower()
    #DEFAULTPW = first_name[0].lower() + last_name[0].lower() + "3456789"
    #NEWFIRST_I_L = first_name[:3].lower()
    #NEWLAST_I_L = last_name[0].lower()
    #DEFAULTPW = NEWFIRST_I_L + last_name.lower() + "123"

    if account_suspended == "True":
        print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("WARNING: ACCOUNT IS SUSPENDED")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print()

    if PW_Flag == "True":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("WARNING: PWFLAG IS SET TO TRUE")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("********************")

    question = str("Do you wish to reset password?")
    choice = query_yes_no(question, default="yes")
    if choice:
        question = "Default password for "+existing_user_name+"?"
        choice = query_yes_no(question, default="yes")
        if choice:
            question = "Is "+existing_user_name+" a STUDENT?"
            choice = query_yes_no(question, default="yes")
            if choice:
                new_password = first_name[:3].lower() + last_name.lower() + "123"
            else:
                print("Creating Teacher Password...")
                #question = "Is "+existing_user_name+" a TEACHER?"
                #choice = query_yes_no(question, default="yes")
                #if choice:
                new_password = first_name[0].lower() + last_name.lower() + "123"
        else:
            custom_pw = input('Input custom password: ')
            new_password = custom_pw

        print("Password will be "+new_password)
        gam_input = "~/bin/gam/gam update user "+existing_user_name+" password '"+new_password+"' changepassword off"
        result = os.popen(gam_input).read()
        print(result)
    print("********************")

    question = str("Do you wish to remove user from ALL OF THEIR GROUPS?")
    choice = query_yes_no(question, default="yes")
    if choice:
        for key in group_dictionary:
            gam_input = "~/bin/gam/gam update group "+key+" remove user "+existing_email
            print(key)
            result = os.popen(gam_input).read()
            print(result)
        gam_input = "~/bin/gam/gam info user "+existing_user_name
        result_1 = os.popen(gam_input).read()
        print(result_1)

        question = "Do you wish to add "+existing_user_name+" back to ALL OF THEIR GROUPS?"
        choice = query_yes_no(question, default="yes")
        if choice:
            for key in group_dictionary:
                print(key)
                gam_input = "~/bin/gam/gam update group "+key+" add "+group_dictionary[key]+" user "+existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)
        else:
            print ("no group addback ")
    print("********************")

    question = str("Do you wish to add "+existing_user_name+" to groups manually?")
    choice = query_yes_no(question, default="yes")
    if choice:

        question = str("Do you wish to add "+existing_user_name+" to groups as REGULAR USER?")
        choice = query_yes_no(question, default="yes")
        if choice:
            question = str("Do you wish to add "+existing_user_name+" to Staff MES as REGULAR USER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mes@mymtsd-vt.org add member user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

            question = str("Do you wish to add "+existing_user_name+" to Staff MMS as REGULAR USER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mms@mymtsd-vt.org add member user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

            question = str("Add "+existing_user_name+" to Staff MHS as REGULAR USER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mhs@mymtsd-vt.org add member user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

        question = str("Do you wish to add "+existing_user_name+" to groups as MANAGER?")
        choice = query_yes_no(question, default="yes")
        if choice:

            question = str("Do you wish to add "+existing_user_name+" to Staff MES as MANAGER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mes@mymtsd-vt.org add manager user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

            question = str("Do you wish to add "+existing_user_name+" to Staff MMS as MANAGER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mms@mymtsd-vt.org add manager user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

            question = str("Do you wish to add "+existing_user_name+" to Staff MHS as MANAGER?")
            choice = query_yes_no(question, default="yes")
            if choice:
                gam_input = "~/bin/gam/gam update group staff-mhs@mymtsd-vt.org add manager user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

    print("********************")

    question = str("Do you wish to move "+existing_user_name+" to a different ORGANIZATIONAL UNIT?")
    choice = query_yes_no(question, default="yes")
    if choice:
        question = str("ACTIVE staff member?")
        choice = query_yes_no(question, default="yes")
        if choice:
            gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Faculty_Staff'"
            result_1 = os.popen(gam_input).read()
            print(result_1)

        question = str("REMOVED staff member?")
        choice = query_yes_no(question, default="yes")
        if choice:
            gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Faculty_Staff/Suspended_Faculty_Staff'"
            result_1 = os.popen(gam_input).read()
            print(result_1)

        else:
            for key in grade_book:
                question = str("Grade: "+str(key)+" Grad Year: "+str(grade_book[key])+" ?")
                choice = query_yes_no(question, default="yes")
                if choice:
                    gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Students/GY20"+str(grad_year)+"'"
                    result_1 = os.popen(gam_input).read()
                    print(result_1)
    print("********************")

    question = str("Do you wish to have "+existing_user_name+" SUSPENDED?")
    choice = query_yes_no(question, default="yes")
    if choice:
        gam_input = "~/bin/gam/gam update user "+existing_email+" suspended on"
        result_1 = os.popen(gam_input).read()
        print(result_1)
    else:
        gam_input = "~/bin/gam/gam update user "+existing_email+" suspended off"
        result_1 = os.popen(gam_input).read()
        print(result_1)
