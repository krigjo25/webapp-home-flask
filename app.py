#  Application entry point

#   Importing required depenedencies
from flask import Flask
from flask_cors import CORS
from flask_session import Session

#   Custom dependencies

from lib.endpoints.github import Github
from lib.utility.logger import AppWatcher
from lib.endpoints.Photos import PhotoLibrary
from lib.endpoints.messages import Announcements
from lib.config import DevelopmentConfig, ProdConfig

# Initialize the logger
logger = AppWatcher()
logger.FileHandler()

#   Initialize Flask app and Extensions
app = Flask(__name__)

#   Configure session to use filesystem (instead of signed cookies)
app.config.from_object(DevelopmentConfig)
Session(app)

CORS(app, resources={r"/*": {"origins": f"*"}})
logger.info(f"App running on {app.config}")

@app.after_request
async def after_request(response):
    """Ensure the responses aren't cached"""
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Expires'] = 0
    response.headers['Paragma'] = 'no-cache'
    
    logger.info(f"Response: {response}")
    return response

#   Endpoints
app.add_url_rule("/", view_func = Announcements().as_view('Index',methods = ["GET"]))
app.add_url_rule("/api/github", view_func = Github().as_view('Github', methods = ["GET"]))
app.add_url_rule("/api/photos", view_func = PhotoLibrary().as_view('Photos', methods = ["POST"]))

#   Webworkers
if __name__ == "__main__":
  app.run()
