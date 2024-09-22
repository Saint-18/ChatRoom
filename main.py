import database
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Route for the root of the web server
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Open the chatroom.html file
    with open("static/chatroom.html", "r") as f:
        # Return the HTML content
        return HTMLResponse(content=f.read())


# Route for other pages in the static directory
@app.get("/{page}", response_class=HTMLResponse)
async def read_root(page):
    # Open the requested page
    with open(f"static/{page}", "r") as f:
        # Return its contents as HTML
        return HTMLResponse(content=f.read())


# API route to retrieve messages from the database
@app.get("/api/messages/get/{chat_id}")
def read_messages(chat_id: int):
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Request messages
        results = database.get_messages(cnx, chat_id)
        # If no results returned
        if not results:
            # Raise a 404 error
            raise HTTPException(
                status_code=404, detail="No messages found in specified chat."
            )
        # Return JSON results
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)


# API route to post new messages to chat
@app.post("/api/messages/create")
async def create_messages(request: Request):
    new_message = await request.json()
    chat_id = new_message.get("chat_id")
    message_body = new_message.get("message_body")
    username = new_message.get("username")
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Insert new message in database
        database.create_message(cnx, chat_id, message_body, username)
        # If error inserting message
        if not results:
            # Raise a 404 error
            raise HTTPException(status_code=404, detail="Unable to create new message.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)

    # Return the updated messages for this chat
    return read_messages(chat_id)
