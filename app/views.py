from app import app

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, abort, request, make_response, send_file, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from pprint import pprint
import json
import papermill as pm
from papermill.exceptions import PapermillExecutionError

import pathlib
import datetime

import os

service_url = os.getenv("SERVICE_URL", "http://localhost")

spec = APISpec(
    title="Covid API",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="Covid API",
        version="1.0.0-oas3",
        contact=dict(
            email="nospam@mailbox.org"
        ),
        license=dict(
            name="Apache 2.0",
            url='http://www.apache.org/licenses/LICENSE-2.0.html'
        )
    ),
    servers=[
        dict(
            description="This API instance",
            url=service_url
        )
    ],
    tags=[
        dict(
            name="Covid",
            description="Endpoints related to Covid"
        )
    ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# class DemoParameter(Schema):
#     gist_id = fields.Int()


# class DemoSchema(Schema):
#     id = fields.Int()
#     content = fields.Str()

#spec.components.schema("Demo", schema=DemoSchema)


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
    out_file = "/tmp/%s.jpg" % region_name
    
    if not check_file_up_to_date(out_file):
        try:
            pm.execute_notebook(
                '/home/jovyan/nb.ipynb',
                '/tmp/output.ipynb',
                parameters = dict(kreis=region_name, output_file=out_file)
            )
        except PapermillExecutionError as e:
            raise ValueError(e)
    
    return send_file(out_file, mimetype='image/jpeg')

def check_file_up_to_date(graph_file):
    fname = pathlib.Path(graph_file)
    if fname.exists():
        mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
        now = datetime.datetime.now()
        return (now - mtime).seconds < (20 * 60)
    else:
        return False

@app.errorhandler(ValueError)
def special_exception_handler(error):
    result = dict(
        error = 'Value Error: %s' % error
    )
    return jsonify(result), 500

# generate the OpenAPI spec
with app.test_request_context():
    spec.path(view=incidence)

openapi_file = '/tmp/openapi.yaml'

with open(openapi_file, 'w') as f:
    f.write(spec.to_yaml())
    f.close()

@app.route("/v3/api-docs", methods=["GET"])
def apidocs():
    return send_file(openapi_file, mimetype='text/x-yaml', as_attachment=True, attachment_filename="openapi.yaml")

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '%s/v3/api-docs' % service_url  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Covid API"
    }
)

app.register_blueprint(swaggerui_blueprint)