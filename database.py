import mysql.connector
import dotenv


def create_database_connection():
    # Read database credentials
    credentials = dotenv.dotenv_values(".env")
    print ("User: ", credentials.get("DATABASE_USER")) #checking if the username and password are being read correctly
    print("Password:", credentials.get("DATABASE_PW"))

    # database configuration information
    config = {
        "user": credentials.get("DATABASE_USER"),
        "password": credentials.get("DATABASE_PW"),
        "host": "127.0.0.1",
        "database": "chatroom",
        "raise_on_warnings": True,
    }
    
    # establish a connection to the database
    cnx = mysql.connector.connect(**config)
    # Return the connection object
    return cnx


def get_messages(cnx: object, chat_id: int):
    """
    Retrieves all message for the requested chatroom
    Input: cnx - MySQL database connection object, chat_id - chatroom identifier
    Returns: Array of JSON objects
    """
    # Create a cursor from the connection object (cnx)
    cursor = cnx.cursor(dictionary=True)

    # Create the database query
    query = (
        "SELECT Users.username, Messages.message_body, Messages.created_at "
        "FROM Messages JOIN Users ON Messages.user_id = Users.user_id JOIN Chats ON Messages.chat_id = Chats.chat_id "
        "WHERE Messages.status = 'approved' AND Chats.chat_id = %s "
        "ORDER BY Messages.created_at;"
    )

    # Execute the query
    cursor.execute(query, (chat_id,))
    # Fetch results
    results = cursor.fetchall()

    return results


def close_database_connection(cnx):
    if cnx.is_connected():
        cnx.close()
