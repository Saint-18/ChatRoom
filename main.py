import database
from typing import Union, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles




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
@app.post("/api/messages/delete/{message_id}")
def delete_message(message_id: int):
    try:
        print(f"Message{message_id}makrked for deletion by a moderator")
        return{"detail: Message marked for deletion"}
    except Exception as e:
        print (f"Error occured :{str (e)}")
        raise HTTPException(status_code=500, detail=f"An error occured: {str (e)}")