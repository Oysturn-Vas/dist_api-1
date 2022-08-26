import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel
import numpy as np

from fastapi import FastAPI

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


cred = credentials.Certificate(
    "coco-sih-firebase-adminsdk-qrhf1-88d3ad8656.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
res = {}


class user_id(BaseModel):
    u_id: str


def euclidian(result):
    result['ADHD'] = (1024-np.linalg.norm(
        np.array((result['ADHD'], result['Anxiety'], result['Depression'], result['Self'], result['Suicide']))-np.array((1024, 0, 0, 0, 0))))/1024*100
    result['Anxiety'] = (1024-np.linalg.norm(
        np.array((result['ADHD'], result['Anxiety'], result['Depression'], result['Self'], result['Suicide']))-np.array((0, 1024, 0, 0, 0))))/1024*100
    result['Depression'] = (1024-np.linalg.norm(
        np.array((result['ADHD'], result['Anxiety'], result['Depression'], result['Self'], result['Suicide']))-np.array((0, 0, 1024, 0, 0))))/1024*100
    result['Self'] = (1024-np.linalg.norm(
        np.array((result['ADHD'], result['Anxiety'], result['Depression'], result['Self'], result['Suicide']))-np.array((0, 0, 0, 1024, 0))))/1024*100
    result['Suicide'] = (1024-np.linalg.norm(
        np.array((result['ADHD'], result['Anxiety'], result['Depression'], result['Self'], result['Suicide']))-np.array((0, 0, 0, 0, 1024))))/1024*100
    return result


@ app.post('/')
async def scoring_endpoint(str_id: user_id):
    result = db.collection('CHATBOT_HISTORY').document(
        str_id.u_id).get()
    if result.exists:
        result = result.to_dict()
        res = euclidian(result)
        return dict(res)

    else:
        return {
            ' ADHD': 0,
            ' Anxiety': 0,
            ' Depression': 0,
            ' Self': 0,
            ' Suicide': 0
        }
