import mysql.connector

def command(cur, cnx): # Admin function for executing an SQL command.
    command_choice = input("Enter 'a' to execute a query command. Enter 'b' to execute a data base editing command (insert, update, delete, etc.)\nInput: ").strip().lower()
    if command_choice == 'a':
        command_string = input("Please enter your SQL command as you would in the workbench (without the semicolon at the end): ")
        try:
            cur.execute(command_string)
            col_names = cur.column_names
            search_result = cur.fetchall()
            print("Search found",len(search_result)," Entries:\n")
            header_size = len(col_names)
            for i in range(header_size):
                print("{:<20s}".format(col_names[i]),end='')
            print()
            print(20*header_size*'-')
            for row in search_result:
                for val in row:
                    print("{:<20s}".format(str(val)),end='')
                print()
        except:
            print("Error. Invalid SQL command entered. Command unsuccesful.\n")

    elif command_choice == 'b':
        command_string = input("Please input your SQL command as you would in the workbench (without the semicolon at the end): ")
        try:
            cur.execute(command_string)
            cnx.commit()
        except:
            print("Error. Invalid SQL command entered. Command unsuccessful.\n")

    else:
        print("Error. Invalid Selection.\n")


def new_script(cur, cnx):
    # Admin function for executing an SQL script.
    admin_script = input("Please enter the entire file name of the script you would like to run (Cannot be used to return data, scripts can only be ran to manipulate data) ")
    file_o = open(admin_script,'r')
    admin_file = file_o.read()
    commands = admin_file.split(';')

    try:
        i = 0
        while i < len(commands):
            cur.execute(("%s" % (commands[i])))
            cnx.commit()
            i = i + 1 
    except:
        print(("%s" % (admin_file)))
        print("An error has occured")

def search(cur):    # Beginning of code created by Theodore Hoang
    loop = True
    yes_no = ["Y","N"]
    while loop == True:
        x = 20
        try_go = True
        print("\nWhich topic would you like to search for?\na. Art Objects\nb. Artists\nc. Quit")
        choice = input("Please enter the letter corresponding to your choice: ").strip().lower()
        if choice == 'a':
                while(True):
                    print("1. Details on paintings\n2. Details on statues\n3. Details on sculptures\n4. Details on other types of art objects\n5. List of all art objects\n6. Return to search menu")
                    art_object = input("Please select which type of art object you are interested in: ")
                    if art_object == "1":
                        ID = input("Enter the ID number of the painting you are looking for (press enter to view all): ") or None
                        if ID == None:
                            instr = "select* from painting"
                            
                        else:
                            instr = "select* from painting where paint_id_no = %(id)s"
                        break

                    elif art_object == "2":
                        ID = input("Enter the ID number of the statue you are looking for (press enter to view all): ") or None
                        if ID == None:
                            instr = "select* from statue"
                        else:
                            instr = "select* from statue where stat_id_no = %(id)s"
                        break
                        
                    elif art_object == "3":
                        ID = input("Enter the ID number of the sculpture you are looking for (press enter to view all): ") or None
                        if ID == None:
                            instr = "select* from sculpture"
                            
                        else:
                            instr = "select* from sculpture where scul_id_no = %(id)s"
                        break
                        
                    elif art_object == "4":    
                        ID = input("Enter the ID number of the other type of art object you are looking for (press enter to view all): ") or None
                        if ID == None:
                            instr = "select* from other"
                            
                        else:
                            instr = "select* from other where other_id = %(id)s"
                        break
                        
                    elif art_object == "5":
                         ID = input("Enter the ID number of the art_object you are looking for (press enter to view all): ") or None
                         ex_choice = input("Would you like to see which exhibition your art piece(s) were shown? (Y or N): ").upper().strip()
                         if ex_choice not in yes_no:
                            print("Invalid input, please try again\n")
                            continue

                         if ex_choice == "Y":
                            if ID == None:
                                instr = "select ID_NO, COLLECTION_NAME, START_DATE,END_DATE, e.EXHIBITION_NAME from shown_during as s, art_object, exhibition as e where art_id_no = id_no and e.exhibition_name = s.exhibition_name"
                            else:
                                instr = "select ID_NO,COLLECTION_NAME ,START_DATE, END_DATE, e.EXHIBITION_NAME from shown_during as s, art_object, exhibition as e where art_id_no = id_no and e.exhibition_name = s.exhibition_name and id_no = %(id)s"

                         elif ID == None:
                            instr = "select ID_NO, EPOCH, YEAR_MADE, CULTURE_OR_COUNTRY, TITLE from art_object"  
                         else:
                            instr = "select ID_NO, EPOCH, YEAR_MADE,CULTURE_OR_COUNTRY, TITLE from art_object where id_no = %(id)s"
                         break
                    
                    elif art_object == "6":
                        try_go = False 
                        break
                        
                    else:
                        print("Invalid selection, please try again")
                    
        elif choice == 'b':
            while(True):
                ID = input("Please enter the name of the artist you are searching for(press enter to view all) or enter \"a\" to return to search menu: ") or None
                if ID == "a":
                    try_go = False 
                    break
                artist_art = input("Would you like to see the the art pieces these artist(s) created? (Y or N): ").upper().strip()
                if artist_art not in yes_no:
                        print("Invalid input, please try again")
                        continue
                if artist_art == "Y" and ID == None:
                    instr = ("select A.ARTIST_NAME, TITLE FROM ART_OBJECT, CREATED_BY AS A, ARTIST AS B WHERE A.ARTIST_NAME = B.ARTIST_NAME AND A.ART_ID_NO = ID_NO")
                    x = x+5
                    break
                elif artist_art == "Y" and ID != None:
                    instr = ("select A.ARTIST_NAME, TITLE FROM ART_OBJECT, CREATED_BY AS A, ARTIST AS B WHERE A.ARTIST_NAME = B.ARTIST_NAME AND A.ART_ID_NO = ID_NO AND A.ARTIST_NAME = %(id)s")
                    x = x+10
                    break
                elif artist_art == "N":
                    instr = "select ARTIST_NAME"
                    art_descr = input("Would you like to see the artist's artist description? (Y or N): ").upper().strip()
                    if art_descr not in yes_no:
                        print("Invalid input, please try again")
                        continue
                    if art_descr == "Y" and ID == None:
                        instr = "select ARTIST_NAME,MAIN_STYLE,ORIGIN_COUNTRY, ARTIST_DESCRIPTION FROM ARTIST"
                        x = x+10
                        break
                    if art_descr == "Y" and ID != None:
                        instr = "select ARTIST_NAME,MAIN_STYLE,ORIGIN_COUNTRY, ARTIST_DESCRIPTION FROM ARTIST WHERE ARTIST_NAME = %(id)s "
                        x = x+10
                        break
                    art_epoch = input("Would you like to see the artist's epoch? (Y or N): ").upper().strip()
                    if art_epoch == "Y":
                        instr = instr + ", EPOCH"
                    art_country = input("Would you like to see the artist's country of origin? (Y or N): ").upper().strip()
                    if art_country == "Y":
                        instr = instr + ", ORIGIN_COUNTRY"
                    art_born = input("Would you like to see the artist's date of birth? (Y or N): ").upper().strip()
                    if art_born == "Y":
                        instr = instr + ", DATE_BORN"
                    art_die = input("Would you like to see the artist's date of death? (Y or N): ").upper().strip()
                    if art_die == "Y":
                        instr = instr + ", DATE_DIED"
                    if art_die not in yes_no or art_born not in yes_no or art_country not in yes_no or art_epoch not in yes_no:
                        print("Invalid input, please try again")
                        continue
                    if ID != None:
                        instr = instr + " from artist where artist_name = %(id)s" 
                    else:
                        instr = instr + " from artist"
                    x = x+5
                    break

        elif choice == 'c':
            print("Exiting query/search mode.")
            main()
        else:
            print("Error. Invalid selection.")
            continue
        
        if try_go == True:
            try:
                if ID != None:
                    cur.execute(instr,{"id":ID})
                else:
                    cur.execute(instr)

            except:
                print("Please try you input again")
        
            rows = cur.fetchall()
            attr_names = cur.column_names
            print()
            for attr in attr_names:
                print("{:<{x}}".format(attr,x=x),end="")
            for row in rows:
                print()
                for col in row:
                    if col == None:
                        col = "Null"
                    print("{:<{x}}".format(col,x=x),end="")
            print() # End of code created by Theodore Hoang


def add(cur, cnx): # Data entry user function for inserting a tuple.

    table_choice = input("Please enter the name of the table that you would like to insert a row into: ")
    cur.execute(("select column_name from information_schema.columns where table_schema = 'ARTSMUSEUM' and table_name = '%s' order by ordinal_position") % (table_choice))
    result = cur.fetchall()
    print(("Please enter the following the values for the following attributes in order: \n %s \n") % (','.join(str(tup) for tup in result)))
    i = 0
    attribute_list = []
    while i < len(result):
        attribute_list.append(input("Please enter the value for a single attribute \n"))
        i = i+1
    
    j = 0 
    i = 1
    execution_string = "INSERT into %s VALUES (" % (table_choice)
    while j < len(result):
        execution_string = execution_string  + " " +"'"+ attribute_list[j]+"'"
        if i < len(result):
            execution_string = execution_string + ","
        i = i + 1
        j = j + 1
    execution_string = execution_string + ")"
    try:
        cur.execute(execution_string)
        print("The following command has been executed %s" % (execution_string))
        cnx.commit()
    except: 
        print("an error has occured")
    
def update(cur, cnx): # Data entry user function for updating information.
    print("UPDATE MENU\nPlease enter the name of the table you would like to update/change.")
    print("\nTABLE NAMES:\n- Art_Object\n- Borrowed\n- Permanent_Collection\n- Painting\n- Statue\n- Sculpture\n- Other\n- Collections\n- Artist\n- Created_By\n- Exhibition\n- Shown_During")
    table = input("Please enter the name of the table you would like to update: ").strip().lower()
    valid_table = True
    identifying_attributes = 1
    if table == "art_object":
        print("You have successfuly selected the ART_OBJECT table for update...")
        id_att_val = input("Please enter the ID number of the art object you would like to update: ").strip()
        id_att = "Id_no"
        print("\nAttributes:\n- Id_no\n- Epoch\n- Art_Description\n- Title\n- Year_Made\n- Culture_Or_Country\n- Collection_Name")
    elif table == "borrowed":
        print("You have successfuly selected the BORROWED table for update...")
        id_att_val = input("Please enter the ID number of the borrowed art object you would like to change: ").strip()
        id_att = "borrow_id_no"
        print("\nAttributes:\n- Borrow_Id_No\n- Date_returned\n- Date_borrowed\n- Collection_Name")
    elif table == "permanent_collection":
        print("You have successfuly selected the PERMANENT_COLLECTION table for update...")
        id_att_val = input("Please enter the ID number of the permanent art object you would like to change: ").strip()
        id_att = "Perm_id_no"
        print("\nAttributes:\n- Perm_Id_No\n- BStatus\n- Cost\n- Date_Acquired")
    elif table == "painting":
        print("You have sucessfuly selected the PAINTING table for update...")
        id_att_val = input("Please enter the ID of the painting you would like to change: ").strip()
        id_att = "Paint_Id_No"
        print("\nAttributes:\n- Paint_Id_No\n- Paint_Style\n- Material\n- Paint_Type")
    elif table == "statue":
        print("You have successfuly selected the STATUE table for update...")
        id_att_val = input("Please enter the ID number of the statue you would like to update: ").strip()
        id_att = "Statue_Id_No"
        print("\nAttributes:\n- Stat_Id_No\n- Stat_Style\n- Stat_Weight\n- Stat_Height\n- Stat_Material")
    elif table == "sculpture":
        print("You have successfuly selected the SCULPTURE table for update...")
        id_att_val = input("Please enter the ID number of the sculpture you would like to change: ").strip()
        id_att = "Scul_Id_No"
        print("\nAttributes:\n- Scul_Id_No\n- Scul_Style\n- Scul_Weight\n- Scul_Height\n- Scul_Material")
    elif table == "other":
        print("You have successfuly selected the OTHER table for update...")
        id_att_val = input("Please enter the ID of the art object you would like to change: ").strip()
        id_att = "Other_Id_No"
        print("\nAttributes:\n- Other_Id\n- Other_Type\n- Other_Style")
    elif table == "collections":
        print("You have successfuly selected the COLLECTIONS table for update...")
        id_att_val = "'" + input("Please enter the name of the collection you would like to update: ").strip() + "'"
        id_att = "CName"
        print("\nAttributes\n- Cname\n- Current_Contact_Person\n- Phone\n- Address\n- CDescription\n CType")
    elif table == "artist":
        print("You have successfuly selected the ARTIST table for update...")
        id_att_val = "'" + input("Please enter the name of the artist you would like to update: ").strip() + "'"
        id_att = "Artist_Name"
        print("\nAttributes:\n- Artist_Name\n- Epoch\n- Origin_Country\n- Date_Born\n- Date_Died\n- Main_Style\n- Artist_Description")
    elif table == "created_by": # Note that logically it does not make much sense to update this table
        print("You have successfuly selected the CREATED_BY table for update...")
        id_att_val = "'" + input("Please enter the name of the artist you would like to change the CREATED_BY table for: ").strip() + "'"
        id_att = "Artist_Name"
        id_att_val2 = input("Please enter the ID of the art object you would like to change the CREATED_BY table for: ").strip()
        id_att2 = "Art_Id_No"
        print("\nAttributes\n- Artist_Name\n- Art_Id_No")
        identifying_attributes = 2
    elif table == "exhibition":
        print("You have successfuly selected the EXHIBITION table for update...")
        id_att_val = "'" + input("Please enter the name of the exhibition you would like to update: ").strip() + "'"
        id_att = "Exhibition_Name"
        print("\nAttributes\n- Exhibition_Name\n- Start_Date\n- End_Date")
    elif table == "shown_during":
        print("You have successfuly selected the SHOWN_DURING table for update...")
        id_att_val = "'" + input("Please enter the name of the exhibiton you would like to change the SHOWN_DURING table for: ").strip() + "'"
        id_att = "Exhibition_Name"
        id_att_val2 = input("Please enter the ID of the art object you would like to change the SHOWN_DURING table for: ").strip()
        id_att2 = "Art_Id_No"
        print("\nAttributes:\n- Exhibition_Name\n- Art_Id_No")
        identifying_attributes = 2
    else:
        print("The table you have selected does not exist in the ORIGINAL database.\nOPTIONS:\na. Proceed with update (new table created in database to be updated)\nb. Quit and re-enter details.")
        mistake_or_new_table = input("Please enter the letter corresponding with your selection: ").strip()
        if mistake_or_new_table == 'a':
            no_of_pks = int(input("Please enter the number of primary keys used to identify a tuple: "))
            if no_of_pks == 1:
                id_att = input("Please enter the name of the primary key attribute").strip()
                id_att_val = input("Please enter the primary key value (ADD APOSTROPHES AROUND STRING DATATYPES, ENTER INTEGERS WITHOUT SURROUNDING APOSTROPHES): ").strip()
            elif no_of_pks == 2:
                id_att = input("Please enter the name of the first primary key attribute: ").strip()
                id_att_val = input("Please enter the first primary key value(ADD APOSTROPHES AROUND NEW STRING AND DATE INPUTS, ENTER INTEGERS WITHOUT SURROUNDING APOSTROPHES): ").strip()
                id_att2 = input("Please enter the name of the second primary key attribute: ").strip()
                id_att_val2 = input("Please enter the second primary key value (ADD APOSTROPHES AROUND NEW STRING AND DATE INPUTS, ENTER INTEGERS WITHOUT SURROUNDING APOSTROPHES): ").strip()
    
        elif mistake_or_new_table == 'b':
            valid_table = False
        else:
            print("Error. Invalid selection.")
    
    if valid_table == True and identifying_attributes == 1:
        change_attribute = input("Please enter the name of the attribute you would like to change: ").strip()
        new_attribute = input("Please enter the new value of the changing attribute (ADD APOSTROPHES AROUND STRING AND DATE INPUTS, ENTER INTEGERS NORMALLY): ").strip()
        try:
            cur.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(table, change_attribute, new_attribute, id_att_val, id_att))
            cnx.commit()
            print("Update on {} was successful.".format(table))
        except mysql.connector.Error:
            print("Error. Invalid input(s) given. Update operation was unsuccessful. Please re-enter values.")
    
    elif valid_table == True and identifying_attributes == 2:
        change_attribute = input("Please enter the name of the attribute you would like to change: ").strip()
        new_attribute = input("Please enter the new value of the changing attribute (ADD APOSTROPHES AROUND NEW STRING AND DATE INPUTS, ENTER INTEGERS WITHOUT SURROUNDING APOSTROPHES): ").strip()
        try:
            cur.execute("UPDATE {} SET {} = {} WHERE {} = {} AND {} = {}".format(table, change_attribute, new_attribute, id_att_val, id_att, id_att_val2, id_att2))
            cnx.commit()
            print("Update on {} was successful.".format(table))
        except mysql.connector.Error:
            print("Error. Invalid input(s) given. Update operation was unsuccessful. Please re-enter values.")

def delete(cur, cnx): # Data entry user function for deleting tuples.
    delete_option = int(input("Input 1 to delete every row of a table\nInput 2 to delete based on a condition\nInput: ").strip())
    delete_from = input("Input the table name you would like to delete from: ").strip()
    if delete_option == 1:
        try:
            cur.execute("delete from {}".format(delete_from))
            cnx.commit()
            print("{0} is now an empty table.".format(delete_from))
        except mysql.connector.Error:
            print("Error. Invalid Inputs.")
    elif delete_option == 2:
        delete_where = input("Input the defining condition: ").strip()
        try:  
            cur.execute("delete from {0} where {1}".format(delete_from, delete_where))
            cnx.commit()
            print("This deletion has been executed.")
        except mysql.connector.Error:
            print("Error. Invalid Inputs.")
    else:
        print("Error")

def admin(cur, cnx):
    print("Welcome to the Arts Museum! You are currently in admin mode.")
    loop = True
    while loop == True:
        print("\nADMIN MENU\na. Enter an SQL command\nb. Provide an SQL script file\nc. Enter data_entry mode\nd. Quit")
        print("Note: You may add, edit, and block users by entering the proper SQL comamnd. You may also make direct changes to the database via entering an SQL command.")
        choice = input("Please enter the letter corresponding to your choice: ").strip().lower()
        if choice == 'a':   # Enter an SQL command
            command(cur, cnx)
        elif choice == 'b': # Enter an SQL script
            new_script(cur, cnx) # May or may not have to remove cur and cnx as passed values to function (not sure if we need it)
        elif choice == 'c':
            data_entry(cur, cnx)
        elif choice == 'd': # Exiting the selection loop
            print("Exiting database. Thank you!")
            loop = False
        
        else:
            print("Error. Invalid selection.")

def data_entry(cur, cnx):
    print("Welcome to the Arts Museum! You are currently in data entry mode.")
    loop = True
    while loop == True:
        print("\nDATA ENTRY MENU\na. Add/Insert Data\nb. Update/Modify Existing Information\nc. Delete Data\nd. Lookup data\ne. Quit")
        choice = input("Please enter the letter corresponding to your choice: ").strip().lower()
        if choice == 'a':   # Add/insert tuples of data
            add(cur, cnx)
        elif choice == 'b': # Update and modify data - Tell user if operation is successful
           update(cur, cnx)
        elif choice == 'c': # Delete tuples of data - Tell user if operation is successful
            delete(cur, cnx)
        elif choice == 'd': # Query for data (same as guest interface)
            search(cur)
        elif choice == 'e': # Exiting the selection loop
            print("Exiting data entry mode. Thank you!")
            loop = False
        else:
            print("Error. Invalid selection.")

def guest(cur):
    print("Welcome to the Arts Museum! You are currently in guest view.")
    loop = True
    while loop == True:
        print("\nGUEST MENU\na. Search for information\nb. Quit")
        choice = input("Please enter the letter corresponding to your choice: ").strip().lower()
        if choice == 'a':
            search(cur)
        elif choice == 'b':
            print("Exiting database. Thank you!")
            loop = False
        else:
            print("Error. Invalid selection.")

def main():
    print("\nARTS MUSEUM DATABASE\n")
    print("MENU - Role Selection:\na. Admin\nb. Data Entry User\nc. Guest")
    role_validity = False
    while role_validity == False:
        role_selection = input("Please enter the letter corresponding to your selection: ").strip().lower()
        if role_selection == 'a' or role_selection == 'b' or role_selection == 'c':
            role_validity = True
        else:
            print("Error. Invalid role selected. Please re-enter your role.")
    
    if (role_selection == 'a') or (role_selection == 'b'):
        connection = False
        while connection == False:
            user_username = input("Please enter your username: ")
            user_password = input("Please enter your password: ")
            try:
                cnx = mysql.connector.connect(
                    host = '127.0.0.1',
                    port = 3306,
                    user = user_username,
                    password = user_password,
                    database = "ARTSMUSEUM")
                if cnx.is_connected():
                    connection = True
            except mysql.connector.Error:
                print("Invalid username or password. Please re-enter details.")
    
    elif role_selection == 'c':
        cnx = mysql.connector.connect(
            host = '127.0.0.1',
            port = 3306,
            user = "guest",
            password = None,
            database = "ARTSMUSEUM")
    
    cur = cnx.cursor(buffered = True)
    cur.execute("use ARTSMUSEUM")
    print()

    if role_selection == 'a':
        admin(cur, cnx)
    elif role_selection == 'b':
        data_entry(cur, cnx)
    else:
        guest(cur)
    
    cnx.close()

if __name__ == "__main__":
    main()
