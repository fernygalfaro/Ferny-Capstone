
import os

class Config:
    SECRET_KEY = os.urandom(24)
    MONGO_URI = 'mongodb+srv://soundscene_user:cats123@cluster0.zx8q6ve.mongodb.net/soundscene_db?retryWrites=true&w=majority'
