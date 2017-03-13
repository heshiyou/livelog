import logging

from channels import Group
from channels.handler import AsgiHandler
from django.http import HttpResponse

import const


logger = logging.getLogger(__name__)


def http_consumer(message):
    response = HttpResponse(pp.pformat(message.content), content_type='text/plain')
    for chunk in AsgiHandler.encode_response(response):
        logger.debug(chunk)
        message.reply_channel.send(chunk)


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group(const.GROUP_NAME).add(message.reply_channel)


def ws_disconnect(message):
    Group(const.GROUP_NAME).discard(message.reply_channel)


def ws_receive(message):
    pass

