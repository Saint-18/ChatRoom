import database
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")


# Route for the root of the web server
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Open the chatroom.html file
    with open("static/login.html", "r") as f:
        # Return the HTML content
        return HTMLResponse(content=f.read())


# Route to handle empty chat page after login
@app.get("/chat", response_class=HTMLResponse)
async def display_chats(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")


# Route to handle dynamically loading chats using Jinja templating
@app.get("/chat/{id}", response_class=HTMLResponse)
async def display_chat_template(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"chat_id": id, "title": "Chat"}
    )


# API route to retrieve messages from the database
# TODO: Convert to POST method to pass body with chat_id and role
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
    message_body = new_message.get("messageText")
    username = new_message.get("username")
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Insert new message in database
        message_created = database.create_message(cnx, chat_id, username, message_body)
        # If error inserting message
        if not message_created:
            # Raise a 404 error
            raise HTTPException(status_code=404, detail="Unable to create new message.")
        return message_created

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)


# Route to login
@app.post("/login")
async def handle_login_request(request: Request):
    login_details = await request.json()
    username = login_details.get("username")
    password = login_details.get("password")
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Insert new message in database
        valid_user = database.validate_user(cnx, username, password)
        # If error inserting message
        if not valid_user:
            # Raise a 403 error
            raise HTTPException(
                status_code=403, detail="Incorrect username or password."
            )
        return valid_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)


# Route to login
@app.post("/api/get/chatlist")
async def get_chatlist(request: Request):
    r = await request.json()
    username = r.get("username")
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Insert new message in database
        chats = database.get_approved_chats(cnx, username)
        # If error inserting message
        if not chats:
            # Raise a 404 error
            raise HTTPException(status_code=404, detail="Unable to retrieve chats.")
        return chats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)


# Route to login
@app.post("/api/messages/delete")
async def remove_message(request: Request):
    r = await request.json()
    message_id = r.get("message_id")
    try:
        # Initialize database connection
        cnx = database.create_database_connection()
        # Insert new message in database
        removed = database.delete_message(cnx, message_id)
        # If error inserting message
        if not removed:
            # Raise a 404 error
            raise HTTPException(status_code=404, detail="Unable to remove message.")
        return removed

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured {str(e)}")
    finally:
        # Ensure the connection exists before attempting to close
        if "cnx" in locals() and cnx:
            database.close_database_connection(cnx)
