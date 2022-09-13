import os
from .urls import app
import uvicorn

def start():
  uvicorn.run(app=app)

# if __name__ == '__main__':
#   uvicorn.run(app=app)