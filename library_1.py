import sqlite3, os, sys, re, time, datetime
createDB = sqlite3.connect('Library.db')
queryCurs = createDB.cursor()
global i
i = 0
global now
now = datetime.datetime.now()

def ReturnBooks():
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Return a Book\n")
	sys.stdout.write("----------------------------------------------\n")
	queryCurs.execute("SELECT ID_Book FROM Loans WHERE ID = '%s'" % str(ID_number).replace("(","").replace(",)",""))
	book_id_list = []
	book_id_list = queryCurs.fetchall()
	if book_id_list == []:
		sys.stdout.write("You are not currently renting any books.\n")
		raw_input()
		main();
	book_list = "\n"
	z = 0
	j = 1
	for item in book_id_list:
		queryCurs.execute("SELECT Book_Title FROM Books WHERE ID_Book = '%s'" % item)
		book_name = queryCurs.fetchone()
		book_list += ("ISBN " + str(book_id_list[z]).replace(",)","") + ". "+ str(book_name).replace("(u'","").replace("u'","").replace("')","")
				.replace("'","").replace('(u"',"").replace('"','')
				.replace(")","")).replace("(","").replace(", u","")
		queryCurs.execute("SELECT Due_Date FROM Loans WHERE ID_Book = '%s'" % book_id_list[z])
		book_due_date = queryCurs.fetchone()
		book_list += (" Due on: "+ str(book_due_date).replace("(u'","").replace("u'","").replace("')","")
				.replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace(",","")+"\n")
		j +=1
		z +=1
	sys.stdout.write(book_list)
	
	choice = raw_input("\nEnter ISBN of book you want to return: ")
	i = 0
	for item in book_id_list:
		if choice == str(item).replace("(","").replace(",)",""):
			i = 1;
	if i == 0:
		sys.stdout.write("You do not currently own this book.")
		raw_input()
		ReturnBooks()
	else:
		queryCurs.execute("UPDATE Books SET ID_Owner = '0' WHERE ID_Book = '%s'" % str(choice))
		createDB.commit()
		queryCurs.execute("UPDATE Loans SET ID = '0' WHERE ID_Book = '%s'" % str(choice))
		createDB.commit()
		queryCurs.execute("SELECT Book_Title FROM Books WHERE ID_Book = '%s'" % str(choice))
		name = queryCurs.fetchone()
		sys.stdout.write("\nYou have returned " + str(name).replace("(u'","").replace("',)","") + "\n")
		sys.stdout.write("Thank you for using the library system!\n\n")
		sys.stdout.write("Press any key to return to the main menu.")
	raw_input()
	main();

def SeeBooks():
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Currently Owned Books\n")
	sys.stdout.write("----------------------------------------------\n")
	queryCurs.execute("SELECT ID_Book FROM Loans WHERE ID = '%s'" % str(ID_number).replace("(","").replace(",)",""))
	book_id_list = []
	book_id_list = queryCurs.fetchall()
	if book_id_list == []:
		sys.stdout.write("You are not currently renting any books.\n")
		raw_input()
		main();
	book_list = ""
	z = 0
	j = 1
	for item in book_id_list:
		queryCurs.execute("SELECT Book_Title FROM Books WHERE ID_Book = '%s'" % item)
		book_name = queryCurs.fetchone()
		book_list += (str(j)+". "+ str(book_name).replace("(u'","").replace("u'","").replace("')","")
				.replace("'","").replace('(u"',"").replace('"','')
				.replace(")","")).replace("(","").replace(", u","")
		queryCurs.execute("SELECT Due_Date FROM Loans WHERE ID_Book = '%s'" % book_id_list[z])
		book_due_date = queryCurs.fetchone()
		book_list += (" Due on: "+ str(book_due_date).replace("(u'","").replace("u'","").replace("')","")
				.replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace(",","")+"\n")
		j +=1
		z +=1
	sys.stdout.write(book_list)
		
		
	book_list = "\n"
	sys.stdout.write("----------------------------------------------\n")
	sys.stdout.write("\nPress any key to return to main menu\n")
	raw_input()
	main();
		
def CheckOutBook():
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Check Out Book\n")
	sys.stdout.write("----------------------------------------------\n")
	sys.stdout.write("Results: ISBN Number: Book Title. Author. Category\n\n")
	q=0
	can_check_out = True
	for items in results:
				sys.stdout.write("ISBN: " + str(results[q])
				.replace("(u'","").replace("u'","").replace("')","").replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace("(","").replace(", u",". ").replace(",",".") + "\n")
				q +=1
	book_ID = raw_input("\nEnter the ISBN number of the book to check it out: ")
	queryCurs.execute("SELECT ID_Book FROM Loans WHERE ID = '%s'" % ID_number)
	test_query = queryCurs.fetchall()
	for item in test_query:
		if book_ID == str(item).replace("(","").replace(",)",""):
			can_check_out = False
	if can_check_out == True:
		queryCurs.execute("SELECT Book_Title FROM Books WHERE ID_Book = '%s'" % book_ID)
		book = queryCurs.fetchone()
		month = now.month+1
		if month == 13:
			month = 1
			year = now.year+1;
		else:
			month = now.month+1
			year = now.year
		sys.stdout.write("You have checked out: %s for 1 month.\n" % str(book).replace("(u'","").replace("',)","")
		.replace('(u"',"").replace('",)',""))
		sys.stdout.write("It will be due on %s" % str(now.day)+"/"+str(month)+"/"+str(year)+"\n")
		queryCurs.execute("UPDATE Books SET ID_Owner = '%(x)s' WHERE ID_Book = '%(y)s'" % {"x": str(ID_number).replace("(","").replace(",)",""), "y":book_ID})
		queryCurs.execute("INSERT INTO Loans(ID,ID_Book,Check_Out_Date,Due_Date) VALUES ('%(x)s','%(y)s','%(z)s','%(q)s')" %
		{"x":str(ID_number).replace("(","").replace(",)",""),"y":book_ID,"z":str(now.day)+"/"+str(now.month)+"/"+str(now.year),"q":str(now.day)+"/"+str(month)+"/"+str(year)})
		createDB.commit()
		sys.stdout.write("Press any key to return to main menu.")
		raw_input()
		main();
	else:
		sys.stdout.write("You already own this book, please select a different one.\n")
		raw_input()
		CheckOutBook();
		
def BookSearch():
	global results
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Book Search\n")
	sys.stdout.write("----------------------------------------------\n")
	sys.stdout.write("1. Search by Title\n")
	sys.stdout.write("2. Search by Author\n")
	sys.stdout.write("3. Search by Category\n")
	decision_2 = raw_input(":")
	
	#decision_2 to Search by choice
	if decision_2 == "1":
		os.system('cls')
		sys.stdout.write("Library DB 1.0 - Book Search\n")
		sys.stdout.write("----------------------------------------------\n")
		search_query = raw_input("Enter Title or Partial Title to search for:\n")
		edited_search_query = ("%" + str(search_query) + "%")
		queryCurs.execute("SELECT ID_Book, Book_Title, Author, Category FROM Books WHERE Book_Title LIKE '%s'" % edited_search_query)
		results = []
		results = queryCurs.fetchall()
		if results != []:
			os.system('cls')
			sys.stdout.write("Library DB 1.0 - Results for '%s'\n" % search_query)
			sys.stdout.write("----------------------------------------------\n")
			sys.stdout.write("Results: ISBN Number: Book Title. Author. Category\n\n")
			q=0
			for items in results:
				sys.stdout.write("ISBN: " + str(results[q])
				.replace("(u'","").replace("u'","").replace("')","").replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace("(","").replace(", u",". ").replace(",",".") + "\n")
				q +=1
			if 	i != 0:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nCheck out one of these books:(C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					CheckOutBook();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
			else:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nLogin to check out a book: (C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					Login();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
		else:
			sys.stdout.write("No results were found for your search - Search Again? (1)\n")
			decision_3 = raw_input(":")
			if decision_3 == ("1"):
				BookSearch();
			else:
				main();
				
	if decision_2 == "2":
		os.system('cls')
		sys.stdout.write("Library DB 1.0 - Author Search\n")
		sys.stdout.write("----------------------------------------------\n")
		search_query = raw_input("Enter Author or Partial Author Name to search for:\n")
		edited_search_query = ("%" + str(search_query) + "%")
		queryCurs.execute("SELECT ID_Book, Book_Title, Author, Category FROM Books WHERE Author LIKE '%s'" % edited_search_query)
		results = []
		results = queryCurs.fetchall()
		if results != []:
			os.system('cls')
			sys.stdout.write("Library DB 1.0 - Results for '%s'\n" % search_query)
			sys.stdout.write("----------------------------------------------\n")
			sys.stdout.write("Results: ISBN Number: Book Title. Author. Category\n\n")
			q=0
			for items in results:
				sys.stdout.write("ISBN: "+ str(results[q])
				.replace("(u'","").replace("u'","").replace("')","").replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace("(","").replace(", u",". ").replace(",",".") + "\n")
				q +=1		
			if 	i != 0:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nCheck out one of these books:(C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					CheckOutBook();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
			else:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nLogin to check out a book: (C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					Login();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
		else:
			sys.stdout.write("No results were found for your search - Search Again? (1)\n")
			decision_3 = raw_input(":")
			if decision_3 == ("1"):
				BookSearch();
			else:
				main();
			
	if decision_2 == "3":
		os.system('cls')
		sys.stdout.write("Library DB 1.0 - Category Search\n")
		sys.stdout.write("----------------------------------------------\n")
		search_query = raw_input("Enter Category to search for:\n")
		queryCurs.execute("SELECT ID_Book, Book_Title, Author, Category FROM Books WHERE Category LIKE '%s'" % search_query)
		results = []
		results = queryCurs.fetchall()
		if results != []:
			os.system('cls')
			sys.stdout.write("Library DB 1.0 - Results for '%s'\n" % search_query)
			sys.stdout.write("----------------------------------------------\n")
			sys.stdout.write("Results: ISBN Number: Book Title. Author. Category\n\n")
			q=0
			for items in results:
				sys.stdout.write("ISBN: "+ str(results[q])
				.replace("(u'","").replace("u'","").replace("')","").replace("'","").replace('(u"',"").replace('"','')
				.replace(")","").replace("(","").replace(", u",". ").replace(",",".") + "\n")
				q +=1		
			if 	i != 0:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nCheck out one of these books:(C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					CheckOutBook();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
			else:
				sys.stdout.write("----------------------------------------------\n")
				sys.stdout.write("\nLogin to check out a book: (C)\n")
				sys.stdout.write("Search again: (S)\n")
				sys.stdout.write("Main Menu: (M)\n")
				decision_3 = raw_input(":")
				if decision_3 == ("c"):
					decision_3 = "C";
				if decision_3 == ("C"):
					Login();
				if decision_3 == ("s"):
					decision_3 = "S";
				if decision_3 == ("S"):
					BookSearch();
				if decision_3 == ("m"):
					decision_3 = "M";
				if decision_3 == ("M"):
					main();
		else:
			sys.stdout.write("No results were found for your search - Search Again? (1)\n")
			decision_3 = raw_input(":")
			if decision_3 == ("1"):
				BookSearch();
			else:
				main();
	else:
		main();

def Registration():
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Registration\n")
	sys.stdout.write("----------------------------------------------\n")
	user_name = raw_input("Please enter your full name: ")
	phone_number = raw_input("Please enter your phone number: ")
	global login_name
	login_name = raw_input("Please choose a login name: ")
	queryCurs.execute('''INSERT INTO Users(Name, phone_number, ID_Books_Checked_Out, Fine_Amounts, Access_Level, Login_Name) VALUES (?,?,?,?,?,?)''',
	(user_name, phone_number, "0", "0", "1", login_name))
	createDB.commit()
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Registration\n")
	sys.stdout.write("----------------------------------------------\n")
	sys.stdout.write("Registration Successful!\n")
	sys.stdout.write("Your login name is " + str(login_name) + "\n")
	queryCurs.execute("SELECT ID FROM Users WHERE login_name = '%s'" % login_name)
	global ID_number
	ID_number = queryCurs.fetchone()
	sys.stdout.write("Your ID number is " + str(ID_number).replace("(","").replace(",)","") + "\n")
	global i
	i = 1
	sys.stdout.write("Press any key to return to main menu\n")
	raw_input()
	main();

def Login():
	os.system('cls')
	sys.stdout.write("Library DB 1.0 - Login\n")
	sys.stdout.write("----------------------------------------------\n")
	global login_name
	login_name = raw_input("Please Enter Login Name: ")
	ID_num = raw_input("Please Enter ID Number: ")
	queryCurs.execute("SELECT ID FROM Users WHERE ID = '%(x)s' AND Login_Name = '%(y)s'" % {"x": ID_num, "y": login_name})
	global ID_number
	ID_number = queryCurs.fetchone()
	if ID_number != None:
		sys.stdout.write("Login Successful!\n")
		global i
		i = 1
		sys.stdout.write("Press Any Key to return to main menu\n")
		raw_input()
		main();
	else:
		sys.stdout.write("Unable to find User; Please register first\n")
		raw_input()
		main();
	
def main():
	os.system('cls')
	sys.stdout.write("Library DB 1.0\n")
	sys.stdout.write("----------------------------------------------\n")
	if i != 0:
		sys.stdout.write("You are logged in as " + str(login_name) + "." + str(ID_number).replace("(","").replace(",)","") + "\n")	
	sys.stdout.write("1. Register (First Time User)\n")
	sys.stdout.write("2. Login\n")
	sys.stdout.write("3. Search And Check Out Books\n")
	sys.stdout.write("4. See Your Currently Checked Out Books\n")
	sys.stdout.write("5. Return a Book\n")
	sys.stdout.write("6. Quits Program\n")
	decision = raw_input(":")
	
	if decision == "1":
		Registration();
	if decision == "2":
		if i != 1:
			Login();
		else:
			sys.stdout.write("You are already logged in. Please choose another option.\n")
			raw_input()
			main();
	if decision == "3":
		BookSearch();
	if decision == "4":
		if i != 0:
			SeeBooks();
		else:
			sys.stdout.write("Please login first to see your currently owned books.\n")
			raw_input()
			main();
	if decision == "5":
		if i != 0:
			ReturnBooks();
		else:
			sys.stdout.write("Please login first to return a currently owned book.\n")
			raw_input()
			main();
	if decision == "6":
		sys.exit();
					
if __name__ == '__main__':
	main()

