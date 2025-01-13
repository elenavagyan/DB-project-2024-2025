import uvicorn
from fastapi import FastAPI
from api import app as api_app
from session import get_db
from data import parse_command, print_unknown, invoke
import asyncio
import json
import datetime
import inspect

from session import engine
from models import Base

# Create all tables
Base.metadata.create_all(bind=engine)

# Create main FastAPI application
app = FastAPI()

# Include the API app from api_update.py
app.mount("/api", api_app)

def to_datetime(input_str: str) -> datetime:
    try:
        return datetime.strptime(input_str, "%Y-%m-%d_%H:%M:%S")
    except ValueError as err:
        raise ValueError(f"Invalid date/time format: {input_str}") from err

# Command line interface to interact with the system
async def handle_command(command: str):
    db = next(get_db())  # Get the database session
    parsed = parse_command(command)

    if not parsed["valid"]:
        print_unknown()
        return

    try:
        # Get the method and arguments from the parsed command
        method = parsed["method"]
        args = parsed["args"]

        # Handle async or sync methods
        if inspect.iscoroutinefunction(method):
            result = await method(*args, db)
        else:
            result = method(*args, db)

        # Print the result
        if result:
            if isinstance(result, list):
                # If the result is a list, print each item on a new line
                for item in result:
                    print(item)
            else:
                # Otherwise, print the result directly
                print(result)
        else:
            print("No result found.")

    except Exception as e:
        print(f"Error executing command: {str(e)}")


if __name__ == "__main__":
    print("Command Line Interface Active. Type 'exit' to quit.")
    while (command := input("Enter command: ")) != "exit":
        asyncio.run(handle_command(command))

# Run the application if executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
