from django.http import request
import mysql.connector
from django.contrib import messages

def getconnection():
    con = mysql.connector.connect(host="localhost", user="root", passwd="", database="resumebuilder")

    if con:
        return con
    else:
        messages.warning(request, "Failed to Connect")
