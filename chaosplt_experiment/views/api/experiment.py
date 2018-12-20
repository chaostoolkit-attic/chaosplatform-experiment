# -*- coding: utf-8 -*-
from uuid import UUID

from flask import abort, Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from chaosplt_experiment.schemas import upload_experiment_schema, \
    experiment_schema, execution_schema, executions_schema

__all__ = ["api"]

api = Blueprint("experiment", __name__)


@api.route('', methods=['POST'])
@login_required
def new():
    user_id = current_user.id
    try:
        payload = upload_experiment_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    org_id = payload["org"]
    workspace_id = payload["workspace"]
    payload = payload["payload"]

    has_org = request.services.account.org.has_org_by_id(org_id=org_id)
    if not has_org:
        return jsonify({
            "message": "Organization is unknown"
        }), 422

    has_workspace = request.services.account.org.has_workspace_by_id(
        org_id, workspace_id=workspace_id)
    if not has_workspace:
        return jsonify({
            "message": "Workspace is unknown in this organization"
        }), 422

    experiment = request.services.experiment.create(
        user_id, org_id, workspace_id, payload)
    return experiment_schema.jsonify(experiment)


@api.route('<uuid:experiment_id>', methods=['GET'])
@login_required
def get(experiment_id: UUID):
    experiment = request.services.experiment.get(experiment_id)
    if not experiment:
        return abort(404)
    return experiment_schema.jsonify(experiment)


@api.route('<uuid:experiment_id>', methods=['DELETE'])
@login_required
def delete(experiment_id: UUID):
    request.services.experiment.delete(experiment_id)
    return "", 204


@api.route('<uuid:experiment_id>/executions', methods=['GET'])
@login_required
def get_executions(experiment_id: UUID):
    experiment = request.services.experiment.get(experiment_id)
    if not experiment:
        return jsonify({
            "message": "Experiment is unknown"
        }), 404
    return executions_schema.jsonify(experiment.executions)


@api.route('executions/<uuid:execution_id>', methods=['GET'])
@login_required
def get_execution(experiment_id: UUID, execution_id: UUID):
    execution = request.services.execution.get(execution_id)
    if not execution:
        return abort(404)
    return execution_schema.jsonify(execution)


@api.route('executions/<uuid:execution_id>', methods=['DELETE'])
@login_required
def delete_execution(experiment_id: UUID, execution_id: UUID):
    request.services.execution.delete(execution_id)
    return "", 204


@api.route('executions/<uuid:execution_id>/journal', methods=['GET'])
@login_required
def get_journal(experiment_id: UUID, execution_id: UUID):
    execution = request.services.execution.get(execution_id)
    if not execution:
        return abort(404)
    return jsonify(execution.payload)
