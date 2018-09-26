"""
Creates public API methods. 
"""
import os
import requests

from skill import Crypto
from skill.metadata import (__version__, __release_date__, __skill_name__, 
                            __skill_description__)

from sanic import response
from sanic.response import json


def create_routes(app):
    """
    Function that creates the application routes.

    Parameters
    ----------
    app: Sanic object
        Initialized Sanic object.

    Returns
    -------
    app: Sanic object
        Modified Sanic app object with routes
        added.

    """
    @app.listener('before_server_start')
    async def init_skill(app, loop):
        """
        Initializes the skill before the server
        starts.
        """
        app.skill = Crypto()
        
    @app.route('/')
    @app.route('/status')
    async def index(request):
        """
        Returns the status of the API.
        """
        r = {
            'success': True, 
            'name': __skill_name__,
            'description': __skill_description__,
            'version': __version__,
            'release_date': __release_date__
        }
        return json(r)

    @app.route('/update')
    async def update(request):
        """
        Returns the status of the API.
        """
        model,model_path,comparison_results = Crypto().model_setting(model_path=None,original=False)
        app.skill.model = model
        app.skill.model_path = model_path
        app.skill.comparison_results = comparison_results
        r = {
            'success': True, 
            'message': f"Model updated successfully. New Model: {app.skill.model}"
        }
        return json(r)
    
    @app.route('/detect', methods=['GET', 'POST', 'OPTIONS'])
    async def estimate(request):
        """
        Produces an estimate on Crypto skill.

        Parameters
        ----------
        text: str
            Identifier for a given article. The identifier
            can be a natural ID or URI.
        
        limit: int 
            Limits the amount of different cryptocurrencies to be found. Default is 3.

        Returns
        -------
        JSON with the summarization results. Results also
        include a list of keywords.
        """
        
        status = None
        if request.method == 'GET':
            success = False
            results = []
            message = 'GET method not supported. Use POST instead.'
            status = 400

        elif request.method == 'OPTIONS':
            success = True
            results = []
            message = 'Endpoint accepts CORS request.'

        elif not request.json:
            success = False
            results = []
            message = 'Make request with JSON object.'
            status = 400

        else:
            text = request.json.get('text')
            limit = request.json.get('limit', 3)
            if not text:
                success = False
                results = []
                message = 'Provide a `text` parameter.'
                status = 400

            else:
                try:
                    results = app.skill.text(text=text, limit=limit)
                    message = 'Searched `text` data successfully.'
                    success = True
                except (ValueError, KeyError) as e:
                    status = 400
                    results = []
                    message = e
                    success = False

        payload = {
            'success': success,
            'message': message,
            'results': results
        }
        return json(payload, status=status or 200)
