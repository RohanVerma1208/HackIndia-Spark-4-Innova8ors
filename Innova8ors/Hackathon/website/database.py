import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-CHL4PUV\\SQLEXPRESS;"  # Escaped the backslash
        "DATABASE=smartforge;"  
        "Trusted_Connection=yes;"              # Using Windows Authentication
    )
    return conn

def get_db_connection2():
    conn2 = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-CHL4PUV\\SQLEXPRESS;"  # Escaped the backslash
        "DATABASE=metadata;"  
        "Trusted_Connection=yes;"              # Using Windows Authentication
    )
    return conn2



