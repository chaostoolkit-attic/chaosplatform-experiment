# -*- coding: utf-8 -*-
from uuid import UUID

from flask import abort, Blueprint, jsonify, request
from flask_login import login_required
from marshmallow import ValidationError

from chaosplt_experiment.schemas import upload_execution_schema, \
    execution_schema

__all__ = ["api"]

api = Blueprint("execution", __name__)


@api.route('', methods=['POST'])
@login_required
def new_execution():
    try:
        payload = upload_execution_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    journal = payload["journal"]
    experiment_id = payload["experiment_id"]

    has_exp = request.services.experiment.has_experiment_by_id(
        experiment_id=experiment_id)
    if not has_exp:
        return jsonify({
            "message": "Experiment is unknown"
        }), 422

    execution = request.services.execution.create(
        experiment_id, journal)
    return execution_schema.jsonify(execution)


@api.route('<uuid:execution_id>', methods=['GET'])
@login_required
def get_execution(execution_id: UUID):
    execution = request.services.execution.get(execution_id)
    if not execution:
        return abort(404)
    return execution_schema.jsonify(execution)


@api.route('<uuid:execution_id>', methods=['DELETE'])
@login_required
def delete_execution(execution_id: UUID):
    request.services.execution.delete(execution_id)
    return "", 204


@api.route('<uuid:execution_id>/journal', methods=['GET'])
@login_required
def get_journal(execution_id: UUID):
    execution = request.services.execution.get(execution_id)
    if not execution:
        return abort(404)
    return jsonify(execution.payload)
