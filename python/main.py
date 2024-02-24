import os
import json
import logging
import pathlib
import hashlib
from fastapi import FastAPI,Path, Form,UploadFile, HTTPException,Query
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "..", "db", "mercari.sqlite3")
items_file = pathlib.Path(__file__).parent.resolve() / "db" / "items.sql"
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def create_table_if_not_exists():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
       )
    ''')
    conn.commit()
    conn.close()

@app.get("/")
def root():
    return {"message": "Hello, world!"}


def get_category_id(category_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Check if category exists
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def create_category(category_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Insert category if not exists
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()

    # Retrieve the category id
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    result = cursor.fetchone()

    conn.close()

    return result[0]


@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    logger.info(f"Receive item: {name}")

    create_table_if_not_exists()

    # Check if the category exists, if not, create it
    category_id = get_category_id(category)
    if not category_id:
        category_id = create_category(category)

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Insert item into the items table
    cursor.execute("INSERT INTO items (name, category_id) VALUES (?, ?)", (name, category_id))

    conn.commit()
    conn.close()

    return {"message": f"item received: {name}"}

@app.get("/items")
def get_items():
    create_table_if_not_exists()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT items.id, items.name, categories.name 
        FROM items 
        INNER JOIN categories ON items.category_id = categories.id
    """)
    items = cursor.fetchall()

    conn.close()

    item_list = [{'id': row[0], 'name': row[1], 'category': row[2]} for row in items]

    return {"items": item_list}

@app.get("/items/{item_id}")
def get_one_item(item_id : int = Path(..., title="The ID of the item to retrieve")):
    create_table_if_not_exists()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {'id': result[0], 'name': result[1], 'category': result[2]}
    else:
        return {"detail": "Item not found"}    

@app.get("/search")
def search_items(keyword: str = Query(..., title="Keyword for search")):
    create_table_if_not_exists()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + keyword + '%',))
    items = cursor.fetchall()

    conn.close()

    item_list = [{'name': row[1], 'category': row[2]} for row in items]

    return {"items": item_list}

@app.get("/image/{image_name}")
async def get_image(image_name):
    # Create image path
    image = images / image_name

    if not image_name.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        
        image = images / "default.jpg"

    return FileResponse(image)
