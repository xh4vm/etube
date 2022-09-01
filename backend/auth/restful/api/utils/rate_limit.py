from flask import request, Response
from http import HTTPStatus
from user_agents import parse
from user_agents.parsers import UserAgent
from jaeger_telemetry.tracer import tracer


@tracer.start_as_current_span('rate_limit::status_response')
def check_error_status_response(response: Response) -> bool:
    return response.status_code != HTTPStatus.OK


@tracer.start_as_current_span('rate_limit::check_bot')
def check_bots() -> bool:
    user_agent: UserAgent = parse(request.headers.get('User-Agent'))
    return user_agent.is_bot or user_agent.get_os() == 'Other' or user_agent.get_device() == 'Other'
