# from typing import List
#
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse
# from typing_extensions import Annotated
#
# app = FastAPI()
#
#
# @app.post("/files/")
# async def create_files(files: Annotated[List[bytes], File()]):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.main import router as db_router
from blog.main import router as blog_router
from admin.main import router as admin_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=db_router,
    prefix='/database',
    tags=['database']
)

app.include_router(
    router=blog_router,
    prefix='',
    tags=['blog']
)

app.include_router(
    router=admin_router,
    prefix='/admin',
    tags=['admin']
)





