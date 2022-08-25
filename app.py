import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel
import numpy as np

from fastapi import FastAPI

app = FastAPI()


class messageItem(BaseModel):
    ADHD: float
    Anixiety: float
    Depression: float
    Self: float
    Sucidal: float

    def euclidian(self):
        self.ADHD = (1024-np.linalg.norm(
            np.array((self.ADHD, self.Anixiety, self.Depression, self.Self, self.Sucidal))-np.array((1024, 0, 0, 0, 0))))/1024*100
        self.Anixiety = (1024-np.linalg.norm(
            np.array((self.ADHD, self.Anixiety, self.Depression, self.Self, self.Sucidal))-np.array((0, 1024, 0, 0, 0))))/1024*100
        self.Depression = (1024-np.linalg.norm(
            np.array((self.ADHD, self.Anixiety, self.Depression, self.Self, self.Sucidal))-np.array((0, 0, 1024, 0, 0))))/1024*100
        self.Self = (1024-np.linalg.norm(
            np.array((self.ADHD, self.Anixiety, self.Depression, self.Self, self.Sucidal))-np.array((0, 0, 0, 1024, 0))))/1024*100
        self.Sucidal = (1024-np.linalg.norm(
            np.array((self.ADHD, self.Anixiety, self.Depression, self.Self, self.Sucidal))-np.array((0, 0, 0, 0, 1024))))/1024*100


@app.post('/')
async def scoring_endpoint(item: messageItem):
    item.euclidian()
    return item


# cred = credentials.Certificate(
#     "coco-sih-firebase-adminsdk-qrhf1-88d3ad8656.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()
# data = {
#     'ADHD': 0,
#     'Depression': 0,
#     'Sucidal': 0,
#     'Anixiety': 0,
#     'Self': 0
# }
# db.collection('users').add(data)
