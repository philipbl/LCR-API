import os
from urllib.parse import quote_plus
import betamax
from betamax_serializers import pretty_json

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

user = os.environ.get('LDS_USER', '')
password = os.environ.get('LDS_PASSWORD', '')

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'
    config.default_cassette_options['record_mode'] = 'once'
    config.default_cassette_options['serialize_with'] = 'prettyjson'

    config.define_cassette_placeholder('<USERNAME>', user)
    config.define_cassette_placeholder('<PASSWORD>', quote_plus(password))
