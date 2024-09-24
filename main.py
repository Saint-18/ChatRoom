import database
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import create_database_connection, get_messages, close_database_connection




app = FastAPI()


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/chatroom.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/{page}", response_class=HTMLResponse)
async def read_root(page):
    with open(f"static/{page}", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/messages/get/{chat_id}")
def read_messages(chat_id: int):
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Get results
        results = database.get_messages(cnx, chat_id)
        if not results:
            raise HTTPException(
                status_code=404, detail="No messages found in specified chat."
            )
        return results

    except Exception as e:
        print (f"Error occured {str (e)}")   #Log the error
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)


@app.post("/api/messages/create")
def create_messages():
    pass


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# marking a message for deletion without removing them from database
# imported "create database connection"and "close database connection" from "database" and update the data in database accordingly.
@app.post("/api/messages/delete/{message_id}")
def delete_message(message_id: int):
     try:
        cnx = create_database_connection()

        # Check if the message exists and update status
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM Messages WHERE message_id = %s", (message_id,))
        message = cursor.fetchone()

        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")

        # Update message status to 'deleted'
        cursor.execute("UPDATE Messages SET status = 'deleted' WHERE message_id = %s", (message_id,))
        cnx.commit()

        print(f"Message {message_id} marked for deletion by a moderator")
        return {"detail": "Message marked for deletion"}
     except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
     finally:
        if "cnx" in locals() and cnx:
            close_database_connection(cnx)