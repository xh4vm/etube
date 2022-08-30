from flask import request, Response, Request
from http import HTTPStatus
from user_agents import parse
from user_agents.parsers import UserAgent


def check_error_status_response(response: Response) -> bool:
    return response.status_code != HTTPStatus.OK


def check_bots() -> bool:
    user_agent = parse(request.headers.get('User-Agent'))
    return user_agent.is_bot