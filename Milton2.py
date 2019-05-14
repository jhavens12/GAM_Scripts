import os
import sys
from itertools import islice
import pprint

grade_book = {'12': 19, '11': 20, '10': 21, '9': 22, '8': 23,'7': 24, \
    '6': 25, '5': 26, '4': 27, '3':28, '2':29, '1':30}

def query_yes_no(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True, 1: True,
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

def multi_choice(question,options):
    #takes in string of question and LIST of options
    #returns chosen value LIST as given
    #Multi-values separated by comma
    choice_dict = {}
    print()
    for n,option in enumerate(options):
        c = n + 1 #avoid 0
        choice_dict[c] = option #create dictionary with number as key
        print(str(c)+": "+option)

    print()
    user_input = input(question+"\nSeparated by commas: ")
    input_list = user_input.split(',') #take multiple input
    numbers = [int(x.strip()) for x in input_list] #add to list

    chosen = []
    for number in numbers:
        chosen.append(choice_dict[number]) #create list of values

    return chosen

print("Milton v2 5/14/19")
print("Starting...")

options = ['Create a new user','Modify Existing User']
choice1 = multi_choice("First Step: What to do?",options)
if 'Create a new user' in choice1:
    print("we will create a new user")

    options = ['Staff','Student']
    choice = multi_choice("Staff or Student?",options)
    if 'Staff' in choice:
        print()
        first_name = input('First Name: ')
        last_name = input('Last Name: ')
        NEWUSER = first_name[0].lower() + last_name.lower()
        NEWEMAIL = NEWUSER + "@mymtsd-vt.org"
        NEWDEFAULTPW = first_name[0].lower() + last_name.lower() + "123"
        gam_input = "~/bin/gam/gam create user "+NEWUSER+" firstname "+first_name+" lastname "+last_name+" password "+NEWDEFAULTPW+" changepassword off org '/Faculty_Staff'"
        #result_1 = os.popen(gam_input).read()
        #print(result_1)

    if 'Student' in choice:
        print()
        first_name = input('First Name: ')
        last_name = input('Last Name: ')
        grade = input('Grade: ')
        grad_year = grade_book[grade]
        NEWUSER = first_name[:3].lower() + last_name.lower()
        NEWEMAIL = NEWUSER + "@mymtsd-vt.org"
        NEWDEFAULTPW = first_name[:3].lower() + last_name.lower() + "123"
        gam_input = "~/bin/gam/gam create user "+NEWUSER+" firstname "+first_name+" lastname "+last_name+" password "+NEWDEFAULTPW+" changepassword off org '/Students/GY20"+str(grad_year)+"'"
        #result_1 = os.popen(gam_input).read()
        #print(result_1)

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

    print("********************")
    print()
if 'Modify Existing User' in choice1:
    print("***MODIFY***")
    print()

    try:
        NEWUSER #check to see if user was just created above
    except NameError: #var not defined
        existing_user_name = input('Username? (just user - no email) ')
    else:#var was defined
        existing_user_name = NEWUSER
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
    if not group_list: #check if group list is empty
        print("NO GROUP MEMBERSHIPS")
    else:
        print("Groups:")
        for x in group_dictionary:
            print(group_dictionary[x], x)
    print()
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

    options = ['PW Reset','Groups: Mass Remove/Add','Groups: Manual','OU Move','Suspend']
    choice = multi_choice("What to do now?",options)
    if 'PW Reset' in choice:
        print("We will reset password")
        question = "Default password for "+existing_user_name+"?"
        sub_choice = query_yes_no(question, default="yes")
        if sub_choice:
            question = "Is "+existing_user_name+" a STUDENT?"
            sub_choice = query_yes_no(question, default="yes")
            if sub_choice:
                new_password = first_name[:3].lower() + last_name.lower() + "123"
            else:
                print("Creating Teacher Password...")
                new_password = first_name[0].lower() + last_name.lower() + "123"
        else:
            custom_pw = input('Input custom password: ')
            new_password = custom_pw

        print("Password will be "+new_password)
        gam_input = "~/bin/gam/gam update user "+existing_user_name+" password '"+new_password+"' changepassword off"
        result = os.popen(gam_input).read()
        print(result)
        print("********************")

    if 'Groups: Mass Remove/Add' in choice:
        question = str("Do you wish to remove user from ALL OF THEIR GROUPS?")
        sub_choice = query_yes_no(question, default="yes")
        if sub_choice:
            for key in group_dictionary:
                gam_input = "~/bin/gam/gam update group "+key+" remove user "+existing_email
                print(key)
                result = os.popen(gam_input).read()
                print(result)
            gam_input = "~/bin/gam/gam info user "+existing_user_name
            result_1 = os.popen(gam_input).read()
            print(result_1)

            question = "Do you wish to add "+existing_user_name+" back to ALL OF THEIR GROUPS?"
            sub_choice = query_yes_no(question, default="yes")
            if sub_choice:
                for key in group_dictionary:
                    print(key)
                    gam_input = "~/bin/gam/gam update group "+key+" add "+group_dictionary[key]+" user "+existing_email
                    result_1 = os.popen(gam_input).read()
                    print(result_1)
            else:
                print ("No group addback ")
        print("********************")

    if 'Groups: Manual' in choice:
        print("Manual group stuff")
        options = ['Member','Manager']
        sub_choice = multi_choice("What type user will they be?",options)
        if 'Member' in sub_choice:
            options = ['fac-staff','faculty-mhs','staff-mhs','faculty-mms','staff-mms','faculty-mes','staff-mes','schoolboard','classroom_teachers']
            sub_sub_choice = multi_choice("Which groups?",options)
            for group in sub_sub_choice:
                print("Adding to group: "+group)
                gam_input = "~/bin/gam/gam update group "+group+" add member user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)

        if 'Manager' in sub_choice:
            options = ['fac-staff','faculty-mhs','staff-mhs','faculty-mms','staff-mms','faculty-mes','staff-mes','schoolboard','classroom_teachers']
            sub_sub_choice = multi_choice("Which groups?",options)
            for group in sub_sub_choice:
                print("Adding to group: "+group)
                gam_input = "~/bin/gam/gam update group "+group+" add manager user "+ existing_email
                result_1 = os.popen(gam_input).read()
                print(result_1)
        print("********************")

    if 'OU Move' in choice:
        print("OU CHANGES BOI")
        options = ['General Staff','Student','Other']
        sub_choice = multi_choice("What type of user?",options)
        if 'General Staff' in sub_choice:
            options = ['Active','Deactivated']
            sub_sub_choice = multi_choice("Status of Staff Member?",options)
            if 'Active' in sub_sub_choice:
                gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Faculty_Staff'"
                result_1 = os.popen(gam_input).read()
                print(result_1)
            if 'Deactivated' in sub_sub_choice:
                gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Faculty_Staff/Suspended_Faculty_Staff'"
                result_1 = os.popen(gam_input).read()
                print(result_1)

        if 'Student' in sub_choice:
            #create list using gradebook
            options = []
            pprint.pprint(grade_book) #show whole grade book
            for key in grade_book:
                options.append(grad_book[key]) #just add year to choices
            sub_sub_choice = multi_choice("Graduation Year?",options)
            cur_grad_year = sub_sub_choice[0] #pull first answer from list
            gam_input = "~/bin/gam/gam update user "+existing_email+" org '/Students/GY20"+str(cur_grad_year)+"'"
            result_1 = os.popen(gam_input).read()
            print(result_1)

        if 'Other' in sub_choice:
            options = ['/Faculty_Staff/IT\ Admins','/Faculty_Staff/Power\ Users','/Faculty_Staff/Service\ Accounts','/Faculty_Staff/Specialty\ Accounts',\
            '/Faculty_Staff/Substitutes','/Faculty_Staff/Student_Teachers','/Students/Internet\ Restriction','/Test']
            sub_sub_choice = multi_choice("Which OU?",options)
            gam_input = "~/bin/gam/gam update user "+existing_email+" org '"+str(sub_sub_choice[0])+"'"
            result_1 = os.popen(gam_input).read()
            print(result_1)

        print("********************")

    if 'Suspend' in choice:
        print("Dealing with suspend")
        question = str("Do you wish to have "+existing_user_name+" SUSPENDED?")
        sub_choice = query_yes_no(question, default="yes")
        if sub_choice:
            gam_input = "~/bin/gam/gam update user "+existing_email+" suspended on"
            result_1 = os.popen(gam_input).read()
            print(result_1)
        else:
            gam_input = "~/bin/gam/gam update user "+existing_email+" suspended off"
            result_1 = os.popen(gam_input).read()
            print(result_1)

        print("********************")
