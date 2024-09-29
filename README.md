# Chat App

A web-based group chat application written for CS410 by Adam Hough, Ritesh Shah, and Eli Ammons.

## Languages and Frameworks

### Frontend

CSS: Handled entirely by TailwindCSS using prebuilt utility classes written directly in HTML.

Javascript: Vanilla JS used for dynamically loading chat messages & sidebar chatroom lists.

### Backend

MySQL: Serves as the database for storing user, chat, membership, and message information.

FastAPI: Python based backend framework for serving pages and routing API calls

Nginix: Used as a reverse proxy

Gunicorn/Uvicorn: ASGI server

### Database

Database schema

![schema.png](Chat%20App%20Project%20102c383b7605800d807bf414f60423e3/schema.png)
