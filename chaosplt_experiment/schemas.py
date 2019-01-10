from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields

__all__ = ["ma", "upload_experiment_schema", "experiment_schema",
           "upload_execution_schema", "execution_schema", "executions_schema",
           "setup_schemas"]

ma = Marshmallow()


def setup_schemas(app: Flask):
    return ma.init_app(app)


class ExperimentSchema(ma.Schema):
    class Meta:
        ordered = True
    id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    org_id = fields.UUID(required=True)
    workspace_id = fields.UUID(required=True)
    created_date = fields.DateTime()
    updated_date = fields.DateTime()
    payload = fields.Dict(keys=fields.String(), allow_none=True)
    url = ma.AbsoluteURLFor('experiment.get', experiment_id='<id>')
    links = ma.Hyperlinks({
        'self': ma.URLFor('experiment.get', experiment_id='<id>')
    })


class UploadExperimentSchema(ma.Schema):
    org = fields.UUID(required=True)
    workspace = fields.UUID(required=True)
    payload = fields.Dict(keys=fields.String(), required=True)


class ExecutionSchema(ma.Schema):
    class Meta:
        ordered = True
    id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    org_id = fields.UUID(required=True)
    workspace_id = fields.UUID(required=True)
    experiment_id = fields.UUID(required=True)
    status = fields.String()
    payload = fields.Dict(keys=fields.String(), allow_none=True)
    url = ma.AbsoluteURLFor(
        'experiment.get_execution', experiment_id='<experiment_id>',
        execution_id='<id>')
    links = ma.Hyperlinks({
        'self': ma.URLFor(
            'experiment.get_execution', experiment_id='<experiment_id>',
            execution_id='<id>')
    })


class UploadExecutionSchema(ma.Schema):
    experiment_id = fields.UUID(required=True)
    journal = fields.Dict(keys=fields.String(), required=True)


upload_experiment_schema = UploadExperimentSchema()
experiment_schema = ExperimentSchema()

upload_execution_schema = UploadExecutionSchema()
execution_schema = ExecutionSchema()
executions_schema = ExecutionSchema(many=True)
