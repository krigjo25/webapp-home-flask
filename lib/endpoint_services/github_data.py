#   Endpoint for the Github repositories

#   Importing libraries
import os, math
from dotenv import load_dotenv
from flask.views import MethodView
from flask import jsonify, request


from lib.apis.github_api import GithubAPI


#   Load environment variables
load_dotenv()

class Github(MethodView):

    def __init__(self, *args, **kwargs):
        pass

    async def get(self):
        response = {}

        #   Ensure the request method is GET
        if request.method == "GET":

            #   Set the response
            response['status'] = 200
            
            response['data'] = await GithubAPI().FetchAPI(os.getenv('GithubRepos'))

            response['page'] = math.ceil(len(response['data']) / 9)
        return jsonify(response)

