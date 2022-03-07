README
Zoe Silverman
Final Lab Assignment
CS 166 / Fall 2021

DESCRIPTION OF PROGRAM
......................
These files make up the final project lab assignment for CS166. The program creates an intranet web application run
through flask. Upon running the application and opening the local host link in a web browser. The user goes straight
to a main menu. At this menu the user can either sign in to an existing account or create a new account. Upon running
the program, three users are automatically added to the database. These users usernames, passwords, and authorization
levels are listed below:

Username: jadams
Password: hHGSD(f2412f*
Authorization Level: 1

Username: gwashington
Password: *saf$aHH23saf$RGG
Authorization Level: 2

Username: jmadison
Password: af*24h)(asdFF
Authorization Level: 3

The 1 authorization level means admin access, and therefore the user can access any menu item. The 2 authorization level
means employer access and therefore the user can access 4/6 of the menu options. The 3 authorization level is an employee
access level, meaning the user can access only 2/4 of the menu options. Upon creation of a new account, the user
automatically has a level 3 authorization level.

For the user login where there is an existing account, the user has only three attempts to login. If the login
credentials are inaccurate (username not in database, username and password do not match) the user will see red error
text appear on their login page. This red text says the number of attempts remaining, and the reason why the login
failed. If the user tries 3 times to login and all three attempts fail, the user is locked out of trying to continue to
log in. When the login is locked, the only way to restart it is to terminate the local host website and then re-run in
the app.py file.

The create new user initial menu option brings the user to a form in which they can create an brand new username and
password. The username is checked against the database to ensure that there are no duplicate usernames. If the username
is unique, the password also must pass several requirements. These requirements include: password maximum characters
validation (25), password minimum characters validation (8), password number validation (must include a number),
password uppercase validation (must include an uppercase letter), password lowercase validation (must include a
lowercase letter), and lastly password special character validation (must include a special character). These
requirements help the user keep their account secure. If the user wants a randomly generated password that meets all
these requirement they can click the button on the screen. A random password will appear below and the user can copy and
paste that into the password form field to create an account.

Regardless of creating a new account or logging into an existing account, the user upon login is brought to the main
menu. The main menu displays the username and the authorization level at the top of the page. There are six options
listed in a radio button form. The user can select which radio button menu option they would like to access, and then
click the blue submit button at the bottom of the form. If the user does not have the proper authorization level to
access said menu item, red text will appear on the top of the page stating the user does not have the proper
authorization to view that menu item. If a user selects a menu option that they are allowed to view, the user is
redirected to that web page.

There is also an option for the user to logout of their account on the bottom of the menu page. If a user clicks that
link they are brought to a new page with a new form. By clicking the button on this page, the user then is able to log
out of the account. Logging out brings the user back to the initial main menu. This resets all variables in the app.py
file to ensure that none of the information associated with the user is accessible after they log out. Logging out also
resets the login attempts, so if they want to log in again, they will have 3 new attempts.

All of the web routes and the flask program are located in the file app.py. Any functions used by the program are
located in the file functions.py. There are also two folders associated with the code. One of the folders, titled
"static" includes two files in it. The first is an image of a lock that is featured on the web page in the top left
corner. The lock image is copyright and royalty free. The source of the image is:
http://www.clker.com/cliparts/a/3/2/a/11949848541326072700padlock_aj_ashton_01.svg.med.png
The second item in the folder is a style.css file which includes all the css that is displayed on the flask web
interface. The other folder is titled "templates". This folder includes 12 html files associated with each page that
could be displayed on the web interface.

There are numerous security measures in place throughout this program. Since all the data is stored in a SQLite
Database, all the queries to access the database are parametrized to avoid any SQL injection that could occur.
Additionally, since this application appears on the web, any links that appear have subresource integrity and include
a sha384 hash to avoid an XXS attack. The password validation as well as the three login attempts additionally make the
program more secure for the users. Additionally, all the passwords that are stored in the database include a 40
character salt as well as hashing. The passwords are hashed through the SHA1. This helps prevent
dictionary and brute force attacks.


INSTRUCTIONS TO RUN
......................
In order to run the program, the user needs all of the following items to exist in the same directory: app.py,
functions.py, "static" folder including style.css and lock.png, and the "templates" folder which includes 12 html
web pages (home.html, userlogin.html, newuseraccount.html, menuoptions.html, menuoption1.html, menuoption2.html,
menuoption3.html, menuoption4.html, menuoption5.html, menuoption6.html, logout.html, and lockedout.html).

When all these files exist in the same directory, the program can be run. To run the program open app.py and run in.
The program will print "Success" three times if the all the SQLite database creation code runs successfully. Then a
Flask app link will appear. The link is title http://localhost:1333/ and runs on the port 1333. To access the web
interface open this link in your up-to-date browser of choice.

You can log in with one of the three existing user accounts listed above to explore what different authorization access
looks like. You can also create a new user account with authorization level 3. From the login you are able to access the
menu items you have authorization to view. Before closing the program and exiting the links, you must click the logout
button of the bottom of the menu. Then you are redirected to the initial web page home, from which you can then close
out of the page. To terminate the local host site, simply close out of app.py and it will terminate the live site.

