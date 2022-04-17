import itertools
import sqlite3

from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#
#     return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

@app.get("/subjects/")
async def get_subjects():
    conn = create_connection(r"S:\teacher_directory\directory_app\db.sqlite3")
    cur = conn.cursor()
    query = "SELECT * FROM teacher_app_subject;"
    cur.execute(query)
    # query_result = [ dict(line) for line in [zip([ column[0] for column in cur.description], row) for row in cur.fetchall()] ]


    result = [dict(rec) for rec in [zip([col[0] for col in cur.description],rec) for rec in cur.fetchall()]]


    return result

@app.get("/teachers/")
async def get_teachers():
    conn = create_connection(r"S:\teacher_directory\directory_app\db.sqlite3")
    cur = conn.cursor()
    query = "SELECT * FROM teacher_app_teacher;"
    cur.execute(query)
    # print()
    result = [dict(rec) for rec in [zip([col[0] for col in cur.description],rec) for rec in cur.fetchall()]]

    return result

