from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

SWAGGER_URL = '/docs' 
API_URL = '/api-docs.yaml' 

@app.route('/api-docs.yaml')
def serve_swagger():
    return send_from_directory(
        DOCS_DIR,
        'api_documentation.yaml',
        mimetype='application/yaml'  
    )

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Finance Manager API",
        'layout': "StandaloneLayout" 
    }
)

app.register_blueprint(swaggerui_blueprint)

if __name__ == '__main__':
    app.run(port=5001, debug=True)