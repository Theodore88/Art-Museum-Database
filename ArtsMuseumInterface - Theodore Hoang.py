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