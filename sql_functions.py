# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 05:24:54 2020

@author: Rory
"""

from datetime import datetime, timedelta, time
import pandas as pd
import mysql.connector
from mysql.connector import errorcode


def users_to_df(config):

    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Read data
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        #print("Read",cursor.rowcount,"row(s) of data.")
        df = pd.DataFrame(rows, columns =['userID', 'name', 'consecutive_days'])
        
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        
        return df
    
    
def items_to_df(config):
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Read data
        cursor.execute("SELECT * FROM items;")
        rows = cursor.fetchall()
        #print("Read",cursor.rowcount,"row(s) of data.")
        df = pd.DataFrame(rows, columns =['item_ID', 'item_name', 'correct', 'userID', 'time'])
        
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        
        return df
    
    
def add_item(item_name, correct, userID, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # insert a data row in the table
        insert_query = """INSERT INTO items (item_name, correct, userID, time) 
                          VALUES (%s, %s, %s, NOW());"""
        
        cursor.execute(insert_query, (item_name, correct, userID))
        #print("Inserted",cursor.rowcount,"row(s) of data.")

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Item Added.")
        

def check_clean(userID, interval, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Check if all returns today are positive:
        fetch_query = """SELECT correct 
                         FROM items
                         WHERE userID = %s AND time >= DATE_SUB(NOW(), INTERVAL %s MINUTE);"""
        cursor.execute(fetch_query, (userID, interval))
        rows = cursor.fetchall()
        #print("Selected",cursor.rowcount,"row(s) of data.")

        if len(rows):
            if all(correct[0] == True for correct in rows) and len(rows):
                #print('Well done!')
                update_query = """UPDATE users
                                  SET consecutive_days = consecutive_days + 1
                                  WHERE userID = %s
                               """
            else:
                #print('Oh dear!')
                update_query = """UPDATE users
                                  SET consecutive_days = 0
                                  WHERE userID = %s
                               """
            cursor.execute(update_query, (userID,))
            #print("Update",cursor.rowcount,"row(s) of data.")
        #else:
            #print('No action...')

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        
        return
    

def get_consecutive_days(userID, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Check if all returns today are positive:
        fetch_query = """SELECT consecutive_days 
                         FROM users
                         WHERE userID = %s;"""
        cursor.execute(fetch_query, (userID,))
        rows = cursor.fetchall()
        #print("Selected",cursor.rowcount,"row(s) of data.")

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        
        return rows[0][0]
    
    
def check_reward(userID, threshold, config):
    num = get_consecutive_days(userID, config)
    if num % threshold and num!=0:
        return False
    else:
        return True
    

def get_history(userID, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Check if all returns today are positive:
        fetch_query = """SELECT item_name, correct, time
                         FROM items
                         WHERE userID = %s;"""
        cursor.execute(fetch_query, (userID,))
        rows = cursor.fetchall()
        #print("Selected",cursor.rowcount,"row(s) of data.")
        
        df = pd.DataFrame(rows, columns = ['item_name', 'correct', 'time'])

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")

        return df
    
    
def clear_items(userID, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Check if all returns today are positive:
        cursor.execute("DELETE FROM items WHERE userID = %s;", (userID,))
        
        update_query = """UPDATE users
                          SET consecutive_days = 0
                          WHERE userID = %s
                       """
        cursor.execute(update_query, (userID,))

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Items Cleared.")

        return

def set_consecutive_days(userID, N, config):
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        #print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        update_query = """UPDATE users
                          SET consecutive_days = %s
                          WHERE userID = %s
                       """
            
        cursor.execute(update_query, (N, userID))
        print('User', str(userID), 'consecutive_days => ' + str(N))

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        
        return