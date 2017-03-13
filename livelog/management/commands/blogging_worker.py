# -*- coding: utf-8 -*-
import json
import logging
import time

from channels import Group
from django.core.management import BaseCommand
from django.conf import settings
import feedparser
import redis

import const

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command to start blogging worker from command line.
    """
    help = 'Fetch and parse RSS feed and send over channel'

    def handle(self, *args, **options):
        rc = redis.Redis(host=settings.REDIS_OPTIONS['HOST'],
                         port=settings.REDIS_OPTIONS['PORT'],
                         db=settings.REDIS_OPTIONS['DB'])
        rc.delete(const.GROUP_NAME)  # flush live blogs
        while True:
            feed = feedparser.parse(const.IFANR_FEED_URL)
            for entry in feed.get('entries')[::-1]:
                if not rc.hexists(const.GROUP_NAME, entry.get('id')):
                    Group(const.GROUP_NAME).send({'text': json.dumps(entry)})
                    rc.hset(const.GROUP_NAME, entry.get('id'), json.dumps(entry))
                    logger.debug('send a message %s ' % entry.get('title'))
                    time.sleep(5)
