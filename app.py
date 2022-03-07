"""
Final Lab Assignment
Zoe Silverman
CS 166 / Fall 2021

This file runs the flask application for a web application in which users can login to a secured system. By running the
file, a link appears which the user can then open in their web browser and then log into the system by either creating
a new account or logging into an existing account. Then the user is able to access menu options upon a successful login.
"""

# import necessary libraries and the functions from functions.py file
from flask import *
import traceback
from functions import *

# declare variables and secret key
app = Flask(__name__)
app.secret_key = "a very super secret key"
username_identification = ''
authorization_identification = 0
login_attempts_remaining = 3


# creation of an app route on the web application for the home page
@app.route('/')
def home():
    return render_template('home.html')


# creation of an app route on the web application for the user login page. Since this page includes a form, there are
# methods included in the app route.
@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    global login_attempts_remaining
    # while loop to ensure that user does not attempt to log into the interface more than 3 times
    while login_attempts_remaining > 1:
        try:
            # if the form is submitted
            if request.method == 'POST':
                # retrive username and password from the form
                username = request.form.get('username')
                password = request.form.get('password')
                login_result, reason = user_login(username, password)
                # if the username and password are included in the database
                if login_result:
                    global username_identification
                    username_identification = username
                    global authorization_identification
                    authorization_identification = int(reason)
                    # send the user to the menu upon a successful login
                    # passes the username and authentication to the main menu
                    return render_template('menuoptions.html', user_account_name=username_identification,
                                           auth_=int(authorization_identification))
                # if the username and password are incorrect
                else:
                    # count this as a failed login attempt
                    login_attempts_remaining = login_attempts_remaining - 1
                    returning_string = 'You have ' + str(login_attempts_remaining) + ' attempts left to login. ' + \
                                       str(reason)
                    try:
                        # send the user back to the login page, but with a warning that displays how many attempts are
                        # left for the user to login to
                        return render_template('userlogin.html', attempts_left=returning_string)
                    except KeyError:
                        pass
            else:
                return render_template('userlogin.html')
        except KeyError:
            pass
    # if the user exceeds three failed login attempts send them to a page that states they are locked out of the system
    return render_template('lockedout.html')


# creation of an app route on the web application for new user login page. This page allows a user to create an account
# with a new username and password. Since this page includes a form, there are methods included in the app route.
@app.route('/newuseraccount', methods=['GET', 'POST'])
def newuseraccount():
    # get a randomly generated password
    generated_password = password_generation()
    try:
        # if a user submit the form
        if request.method == 'POST':
            # set the submitted username and password
            username = request.form.get('username')
            password = request.form.get('password')
            # attempt to add new user to the database
            result, reasoning = add_user(username, password)
            # if user is successfully added with no issue
            if result:
                global username_identification
                username_identification = username
                global authorization_identification
                # authorization as the lowest possible level
                authorization_identification = 3
                # send the user to the menu options web page and pass the authorization level as well as the username
                return render_template('menuoptions.html', user_account_name=username,
                                       auth_=int(authorization_identification))
            else:
                # if the new user add function failed, return the user to the newuseraccount page and give explaining
                # as to why the process failed
                try:
                    return render_template('newuseraccount.html', reason_for_failure=reasoning,
                                           random_password=generated_password)
                except KeyError:
                    pass
        else:
            # render the newuseracount web page
            return render_template('newuseraccount.html', random_password=generated_password)
    except KeyError:
        pass


# creation of an app route on the web application for main menu with different menu options displayed. Since this page
# includes a form, there are methods included in the app route.
@app.route('/menuoptions', methods=['GET', 'POST'])
def menuoptions():
    global username_identification
    global authorization_identification
    try:
        # if a user selects a menu option
        if request.method == 'POST':
            menu_selection = request.form['menuoptions']
            # render template for menuoption 1 and send username and authorization level
            if menu_selection == 'menuoption1':
                return render_template('menuoption1.html', user_account_name=username_identification,
                                       auth_=int(authorization_identification))

            # render template for menuoption 2 and send username and authorization level
            elif menu_selection == 'menuoption2':
                return render_template('menuoption2.html', user_account_name=username_identification,
                                       auth_=int(authorization_identification))

            # if user selects menu option 3
            elif menu_selection == 'menuoption3':
                # check authorization level
                if authorization_identification in [1, 2]:
                    # render template for menuoption 3 and send username and authorization level
                    return render_template('menuoption3.html', user_account_name=username_identification,
                                           auth_=int(authorization_identification))
                # if user does not have proper authorization return them to the main menu and issue an authorization
                # warning
                else:
                    return render_template('menuoptions.html', auth_issue='You do not have the authorization level to '
                                                                          'access this menu option.',
                                           user_account_name=username_identification,
                                           auth_=int(authorization_identification))

            # if user selects menu option 4
            elif menu_selection == 'menuoption4':
                # check authorization level
                if authorization_identification in [1, 2]:
                    # render template for menuoption 4 and send username and authorization level
                    return render_template('menuoption4.html', user_account_name=username_identification,
                                           auth_=int(authorization_identification))
                # if user does not have proper authorization return them to the main menu and issue an authorization
                # warning
                else:
                    return render_template('menuoptions.html', auth_issue='You do not have the authorization level to '
                                                                          'access this menu option.',
                                           user_account_name=username_identification,
                                           auth_=int(authorization_identification))

            # if user selects menu option 5
            elif menu_selection == 'menuoption5':
                # check authorization level
                if authorization_identification in [1]:
                    # render template for menuoption 5 and send username and authorization level
                    return render_template('menuoption5.html', user_account_name=username_identification,
                                           auth_=int(authorization_identification))
                else:
                    # if user does not have proper authorization return them to the main menu and issue an authorization
                    # warning
                    return render_template('menuoptions.html', auth_issue='You do not have the authorization level to '
                                                                          'access this menu option.',
                                           user_account_name=username_identification,
                                           auth_=int(authorization_identification))

            # if user selects menu option 6
            elif menu_selection == 'menuoption6':
                # check authorization level
                if authorization_identification in [1]:
                    # render template for menuoption 6 and send username and authorization level
                    return render_template('menuoption6.html', user_account_name=username_identification,
                                           auth_=int(authorization_identification))
                else:
                    # if user does not have proper authorization return them to the main menu and issue an authorization
                    # warning
                    return render_template('menuoptions.html', auth_issue='You do not have the authorization level to '
                                                                          'access this menu option.',
                                           user_account_name=username_identification,
                                           auth_=int(authorization_identification))

            else:
                # if user does not have proper authorization return them to the main menu and issue an authorization
                # warning
                return render_template('menuoptions.html', auth_issue='You do not have the authorization level to '
                                                                      'access this menu option.',
                                       user_account_name=username_identification,
                                       auth_=int(authorization_identification))

        # render menu options web page with username and authorization displayed
        else:
            return render_template('menuoptions.html', user_account_name=username_identification,
                                   auth_=int(authorization_identification))
    except KeyError:
        pass


# creation of an app route on the web application for menu option 1
@app.route('/menuoption1')
def menuoption1():
    return render_template('menuoption1.html')


# creation of an app route on the web application for menu option 2
@app.route('/menuoption2')
def menuoption2():
    return render_template('menuoption2.html')


# creation of an app route on the web application for menu option 3
@app.route('/menuoption3')
def menuoption3():
    return render_template('menuoption3.html')


# creation of an app route on the web application for menu option 4
@app.route('/menuoption4')
def menuoption4():
    return render_template('menuoption4.html')


# creation of an app route on the web application for menu option 5
@app.route('/menuoption5')
def menuoption5():
    return render_template('menuoption5.html')


# creation of an app route on the web application for menu option 6
@app.route('/menuoption6')
def menuoption6():
    return render_template('menuoption6.html')


# creation of an app route on the web application for the logout web page. The user can decided if they want to logout
# of their account. Since this page includes a form, there are methods included in the app route.
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # if the user chooses to logout
    try:
        if request.method == 'POST':
            # reset all variables
            global username_identification
            username_identification = ''
            global authorization_identification
            authorization_identification = 0
            global login_attempts_remaining
            login_attempts_remaining = 3
            # send the user to the homepage
            return render_template('home.html')
        else:
            # display the logout page with the username and authorization level
            return render_template('logout.html', user_account_name=username_identification,
                                   auth_=int(authorization_identification))
    except KeyError:
        pass


# creation of an app route on the web application for the locked out web page that appears if a user tries to login to
# their account 3 times
@app.route('/lockedout')
def lockedout():
    return render_template('lockedout.html')


# run the web application on port 1333 for a locally hosted site
if __name__ == '__main__':
    try:
        app.run(debug=app.debug, host='localhost', port=1334)
    except Exception as err:
        traceback.print_exc()
