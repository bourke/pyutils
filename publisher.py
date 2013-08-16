from womack import publish, config as wconfig
from yaml_config import YamlConfig

config = YamlConfig('config.yaml')

use_womack = config.get('USE_WOMACK', True)

print "using womack", use_womack

wconfig.config.port = config.get('WOMACK_PORT', 8111)
wconfig.config.host = config.get('WOMACK_HOST', '0.0.0.0')

publisher = publish.Publisher()

