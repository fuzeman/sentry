from __future__ import absolute_import

from sentry.utils.safe import trim
from sentry.utils.strings import truncatechars, strip

from .base import BaseEvent


class ErrorEvent(BaseEvent):
    key = 'error'

    def has_metadata(self):
        return 'sentry.interfaces.Exception' in self.data

    def get_metadata(self):
        exception = self.data['sentry.interfaces.Exception']['values'][-1]

        # Retrieve message
        message_interface = self.data.get('sentry.interfaces.Message', {
            'message': self.data.get('message', ''),
        })

        message = strip(message_interface.get('formatted', message_interface['message']))
        
        # Pick event value
        if message:
            value = truncatechars(message.splitlines()[0], 100)
        else:
            value = trim(exception.get('value', ''), 1024)
        
        # Build metadata
        return {
            'type': trim(exception.get('type', 'Error'), 128),
            'value': value,
            'message': message,
        }

    def to_string(self, metadata):
        if metadata.get('message'):
            return metadata['message']

        if metadata.get('title'):
            return metadata['title']

        if metadata.get('type') and metadata.get('value'):
            return u'{}: {}'.format(
                metadata['type'],
                truncatechars(metadata['value'].splitlines()[0], 100),
            )

        if metadata.get('type'):
            return metadata['type']

        return '<unlabeled event>'
