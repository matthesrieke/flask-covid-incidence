from app import app, openapi, service

from flask import Flask, abort, request, make_response, send_file, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

import os

service_url = os.getenv("SERVICE_URL", "http://localhost")
openapi_file = '/tmp/openapi.yaml'
API_URL = '%s/v3/api-docs' % service_url  # Our API url (can of course be a local resource)

@app.route("/incidence", methods=["GET"])
def incidence():
    """incidence of the last 7 days (per 100,000 population).
    ---
    get:
      parameters:
      - in: query
        name: region
        schema:
          type: string
      responses:
        200:
          description: the graph as JPEG
          content:
            image/jpeg:
              schema:
                type: string
                format: binary

    """
    
    region_name = request.args.get('region')
    out_file = service.get_incidence_graph(region_name)
    
    return send_file(out_file, mimetype='image/jpeg')

@app.errorhandler(ValueError)
def special_exception_handler(error):
    result = dict(
        error = 'Value Error: %s' % error
    )
    return jsonify(result), 500


@app.route("/v3/api-docs", methods=["GET"])
def apidocs():
    return send_file(openapi_file, mimetype='text/x-yaml', as_attachment=True, attachment_filename="openapi.yaml")

# generate the OpenAPI spec
with app.test_request_context():
    openapi.spec.path(view=incidence)

with open(openapi_file, 'w') as f:
    f.write(openapi.spec.to_yaml())
    f.close()

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    "/v3/swagger-ui",  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Covid API"
    }
)

app.register_blueprint(swaggerui_blueprint)
