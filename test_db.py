import os
import pyodbc
from dotenv import load_dotenv

def test_database_connection():
    print("🔍 Testing Azure SQL Database Connection...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get database credentials
    server = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    print(f"Server: {server}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    
    try:
        # Create connection string
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        
        # Attempt connection
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Test simple query
        cursor.execute("SELECT @@VERSION;")
        row = cursor.fetchone()
        
        print("✅ Database connection SUCCESSFUL!")
        print(f"SQL Server Version: {row[0]}")
        
        # Close connection
        cursor.close()
        connection.close()
        
        return True
        
    except pyodbc.InterfaceError as e:
        print("❌ ODBC Driver Error - Driver may not be installed")
        print(f"Error: {e}")
        print("\n💡 Install ODBC Driver 17 for SQL Server from:")
        print("https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        
    except pyodbc.OperationalError as e:
        print("❌ Connection Error - Check firewall rules and credentials")
        print(f"Error: {e}")
        print("\n💡 Check:")
        print("1. SQL Server firewall allows your IP")
        print("2. Database credentials are correct")
        print("3. Server name is correct")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    return False

if __name__ == "__main__":
    test_database_connection()