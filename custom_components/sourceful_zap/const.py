from datetime import timedelta

DOMAIN = "sourceful_zap"
DEFAULT_NAME = "Zap"
DEFAULT_HOST = "zap.local"
DEFAULT_ENDPOINT = "/api/data/p1/obis"
DEFAULT_SYSTEM_ENDPOINT = "/api/system"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)

CONF_ENDPOINT = "endpoint"
CONF_SYSTEM_ENDPOINT = "system_endpoint"
