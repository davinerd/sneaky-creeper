"""
Contains classes for channels and encoders to inherit from.
"""
from sneakers.errors import ExfilChannel, ExfilEncoder

"""
Parameter Class

Handles the possible parameters that can be passed to each channel.
"""


class Parameter(object):
    def __init__(self, name, required, description, default=None):
        self.name = name
        self.required = required
        self.description = description
        self.default = default
        self.value = None


"""
Module Class

Used as the base for both Channel and Encoder classes
"""


class Module(object):
    # Param objects go here
    params = {
        'sending': [
        ],
        'receiving': [
        ]
    }

    info = {
        "name": "Module name",
        "author": "sneaky-creeper",
        "description": "A description goes here",
        "comments": ["add something", "and something else"]
    }

    def __init__(self):
        pass

    def param(self, paramType, name):
        # Get a parameter
        print(self.params)
        for p in self.params[paramType]:
            print(p)
            if p.name == name:
                return p.value

    def set_params(self, params):
        if not isinstance(params, dict):
            raise TypeError("Module parameters must be specified as a dictionary.")

        for paramType in ['sending', 'receiving']:
            if paramType not in params:
                # the params passed don't have 'sending' or 'receiving' block
                continue
            for param in self.params[paramType]:
                # each param attempts to fetch its value from values passed in
                try:
                    param.value = params[paramType][param.name]
                except:
                    pass

        for paramType in ['sending', 'receiving']:
            # now check to make sure all the required params are set
            # (in a diffent for block because of the if/continue above)
            missing = []
            for param in self.params[paramType]:
                if param.required and param.value is None:
                    missing.push('param.name')
            if len(missing) > 0:
                raise ValueError("Required parameter(s) {} not set for {}.".format(missing.join(', '), paramType))


"""
Channel Class

To create a new channel, create a new file named yourChannelName.py
with a class YourChannelName that inherits from this base class.
"""


class Channel(Module):
    # maximum length of characters of each transmission
    # useful in case of media limitations (i.e. Twitter)
    maxLength = 140

    # maximum number of posts per hour
    maxHourly = 100

    opsecSafe = False

    def __init__(self):
        Module.__init__(self)

    # TODO
    # set up a way to pass just sending
    # or just receiving params to these functions
    # (instead of accessing all params)
    def send(self, data):
        pass

    def receive(self):
        pass

    def set_params(self, params):
        for k in params.keys():
            if 'sending' not in k and 'receiving' not in k:
                raise ExfilChannel('Missing sending and/or receiving for channel {0}'.format(self.__class__.__name__))
            for param in self.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilChannel(
                        'Missing required parameter \'{0}\' for channel \'{1}\' ({2}).'.format(param,
                                                                                               self.__class__.__name__,
                                                                                               k))
                self.reqParams[k] = params[k]


"""
Encoder Class

To create a new encoder, create a new file named yourEncoderName.py
with a class YourEncoderName that inherits from this base class.
"""


class Encoder(Module):
    def __init__(self):
        Module.__init__(self)

    # TODO
    # set up params such that each function
    # only has access to encode/decode params
    def encode(self, data):
        pass

    def decode(self, data):
        pass

    def set_params(self, params):
        for k in params.keys():
            if 'encode' not in k and 'decode' not in k:
                raise ExfilEncoder('Missing encode and/or decode for decoder {0}'.format(self.__class__.__name__))
            for param in self.requiredParams[k]:
                if param not in params[k]:
                    raise ExfilEncoder(
                        'Missing required parameter \'{0}\' for encoder \'{1}\' ({2}).'.format(param,
                                                                                               self.__class__.__name__,
                                                                                               k))
                self.reqParams[k] = params[k]
