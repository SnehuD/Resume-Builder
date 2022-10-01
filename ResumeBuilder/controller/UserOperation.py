from controller import connection


# Register User
def reg_user(u):
    reg_query = "insert into user (id, fname, lname, email, pass, token, evs) values (%s, %s, %s, %s, %s, %s, " \
                "'Inactive') "
    con = connection.getconnection()
    register = con.cursor()
    register.execute(reg_query, u)
    con.commit()
    return register.rowcount


# check Id Or Email is Exist Or Not
def check_id_email(uid, email):
    con = connection.getconnection()
    chk_query = "select id, email from user where id=%s or email=%s"
    chk = con.cursor()
    user = (uid, email)
    chk.execute(chk_query, user)
    for dt in chk:
        if dt[0] == uid or dt[1] == email:
            return 1
        else:
            return 0


# Login Here
def login(email, passwd):
    con = connection.getconnection()
    login_query = "select email,pass from user where email=%s and pass=%s"
    credentials = con.cursor()
    cred = (email, passwd)
    credentials.execute(login_query, cred)
    for dt in credentials:
        if dt[0] == email and dt[1] == passwd:
            return 1
        else:
            return 0


# Check Email Verification Status
def check_evs(email):
    con = connection.getconnection()
    chk = con.cursor()
    chk_query = "select evs from user where email=%s"
    chk.execute(chk_query, (email,))
    for row in chk:
        if row[0] != "Inactive":
            return 1
        else:
            return 0
    con.commit()


# Verify Email
def verify_email(uid, token):
    con = connection.getconnection()
    ver = con.cursor()
    query = "select id, token from user where id=%s"
    ver.execute(query, (uid,))
    row = ver.fetchone()
    print(ver.rowcount)
    if ver.rowcount == 1:
        for dt in row:
            if str(row[0]) == uid and str(row[1]) == token:
                update_evs(uid)
                return 1
            else:
                return 0
    else:
        return 0
    con.commit()


# Update EVS Active
def update_evs(uid):
    con = connection.getconnection()
    up = con.cursor()
    evs_query = "update user set evs='Active' where id=%s"
    up.execute(evs_query, (uid,))
    con.commit()


# Get Resend Credentials
def resend_credentials(email):
    con = connection.getconnection()
    mycursor = con.cursor()
    query = "select id, token from user where email=%s"
    mycursor.execute(query, (email,))
    row = mycursor.fetchone()
    for dt in row:
        return row[0], row[1]


# Check Email Exist or Not
def check_email(email):
    con = connection.getconnection()
    check = con.cursor()
    check_query = "select email from user where email=%s"
    check.execute(check_query, (email,))
    for dt in check:
        if dt[0] == email:
            return 1
        else:
            return 0


# Get Password
def getPasswd(email):
    con = connection.getconnection()
    getpass = con.cursor()
    getpass_query = "select pass from user where email=%s"
    getpass.execute(getpass_query, (email,))
    for passwd in getpass:
        return passwd


# Get Profile
def get_profile(email):
    con = connection.getconnection()
    getprofile = con.cursor()
    get_query = "select *from user where email=%s or id=%s"
    getprofile.execute(get_query, (email, email))
    for profile in getprofile:
        return profile


# Update Profile
def update_profile(up_details):
    con = connection.getconnection()
    update = con.cursor()
    update_query = "update user set fname=%s, lname=%s, pass=%s where id=%s"
    update.execute(update_query, up_details)
    con.commit()
    return update.rowcount


# Delete Profile
def delete_profile(id):
    con = connection.getconnection()
    delete = con.cursor()
    delete_query = "delete from user where id = %s"
    delete.execute(delete_query, (id,))
    con.commit()
    return delete.rowcount
