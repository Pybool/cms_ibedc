# connection_executor.py
from django.db import connection

def fetch_one(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
    return row

def fetch_all(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return rows

def dict_fetch_all(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall_util(cursor)
    return rows

def dictfetchall_util(cursor):
    """
    Return all rows from a cursor as a list of dictionaries
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
    # Print the results and the last page number
    print(results)
    last_page = cursor.fetchone()[0]
    print(last_page)