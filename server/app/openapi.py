from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
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
