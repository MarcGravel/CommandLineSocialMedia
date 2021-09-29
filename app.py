import mariadb
import dbcreds

conn = None
cursor = None
db_pwd = None

while True:
    print("Choose an option:")
    print("1. Login")
    print("2. Sign up")
    auth_choice = input()

    if auth_choice == "1":
        print("Please Log In:")
        user_name = input("Enter username: ")
        user_pwd = input("Enter password: ")
        break
    elif auth_choice == "2":
        print("Please Sign up:")
        sign_up_name = input("Enter username: ")
        sign_up_pwd = input("Enter password: ")

        try:
            conn = mariadb.connect(
                            user=dbcreds.user,
                            password=dbcreds.password,
                            host=dbcreds.host,
                            port=dbcreds.port,
                            database=dbcreds.database
                            )
            cursor = conn.cursor()

            cursor.execute("SELECT alias FROM hackers WHERE alias=?", [sign_up_name])
            result = cursor.fetchone()
            if result == None:
                cursor.execute("INSERT INTO hackers(alias, password) VALUES(?,?)", [sign_up_name, sign_up_pwd])
                conn.commit()
                user_name = sign_up_name
                user_pwd = sign_up_pwd
                print("Signed up and logged in!")
                print()
                break
            else: 
                print("That username is already taken, try again.")
                print()
        except mariadb.DataError:
            print("Something is wrong with your data")
        except mariadb.OperationalError:
            print("Something is wrong with your connection")
        except mariadb.ProgrammingError:
            print("Code error, check the code")
        except mariadb.IntegrityError:
            print("Query negatively affects the integrity of the database.")
        except:
            print("Something went wrong")
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()    
    else:
        print("That wasnt an option. Try again")  

conn = None
cursor = None

try:
    conn = mariadb.connect(
                            user=dbcreds.user,
                            password=dbcreds.password,
                            host=dbcreds.host,
                            port=dbcreds.port,
                            database=dbcreds.database
                            )
    cursor = conn.cursor()

    #gets all alias (they are UNIQUE KEY'd in db)
    cursor.execute("SELECT alias FROM hackers")
    all_users = cursor.fetchall()

    #If there is a matching alias in db, will grab the corresponding pwd from db
    if (any(user_name in a for a in all_users)):
        cursor.execute("SELECT password FROM hackers WHERE alias=?", [user_name])
        db_pwd = cursor.fetchone()[0]

except mariadb.IntegrityError:
    print("Your query would have broken the database and we stopped it")
except:
    print("Something went wrong")

#Checks if db pass matches user input pass
if db_pwd == user_pwd:
    while True:
        print("Which option would you like?")
        print("1. Enter a new exploit")
        print("2. See all of your exploits")
        print("3. See all others exploits")
        print("4. Exit application")
        user_choice = input("What is your choice: ")

        try:
            #gets current users user id for SQL queries below
            cursor.execute("SELECT id FROM hackers WHERE alias=?", [user_name])
            current_user_id = cursor.fetchone()[0]
            
            #print for spacing
            print()

            if user_choice == "1":
                print("Please write your exploit.")
                new_exploit = input()
                #enters content into exploits table with matching user id from current user into the FK column
                cursor.execute("INSERT INTO exploits(content, user_id) VALUES(?,?)", [new_exploit, current_user_id])
                conn.commit()
                print("The exploit has been submitted")
            elif user_choice == "2":
                #gets all content from exploits table that have user id matching current users id
                cursor.execute("SELECT content FROM exploits WHERE user_id=?", [current_user_id])
                users_content_list = cursor.fetchall()
                for content in users_content_list:
                    print(content)
            elif user_choice == "3":
                #selects all content from exploits table EXCEPT the content that has matching id to current users id
                cursor.execute("SELECT content FROM exploits EXCEPT SELECT content FROM exploits WHERE user_id=?", [current_user_id])
                others_content_list = cursor.fetchall()
                for content in others_content_list:
                    print(content)
            elif user_choice == "4":
                exit_choice = input("Are you sure you want to exit? Y/N: ")
                if(exit_choice == "Y" or exit_choice == "y"):
                    print("GoodBye!")
                    break
                elif(exit_choice == "N" or exit_choice == "n"):
                    pass
                else: 
                    print("I am just going to assume you want to leave. Bye.")
                    break
            else:
                print("Please enter a choice between 1 and 4")
            
            #print for spacing
            print()
        
        except mariadb.DataError:
            print("Something is wrong with your data")
        except mariadb.OperationalError:
            print("Something is wrong with your connection")
        except mariadb.ProgrammingError:
            print("Code error, check the code")
        except mariadb.IntegrityError:
            print("Query negatively affects the integrity of the database.")
        except:
            print("Something went wrong")

else: 
    print("Incorrect credentials. Closing program")

if (cursor != None):
    cursor.close()
if (conn != None):
    conn.rollback()
    conn.close()