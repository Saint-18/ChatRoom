import database
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
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


# TODO: Create a route to save messages to the database
@app.post("/api/messages/create")
def create_messages():
    # Skip for now
    pass
