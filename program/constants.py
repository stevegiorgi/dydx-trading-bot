from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# SELECT MODE
MODE = "DEVELOPMENT"

# CLOSE ALL POSITIONS
ABORT_ALL_POSITIONS = False

# FIND COINTEGRATED PAIRS
FIND_COINTEGRATED = False

# PLACE TRADES
PLACE_TRADES = True

# RESOLUTION
RESOLUTION = "1HOUR"

# STATS WINDOW
WINDOW = 21

# THRESHOLDS - OPENING
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 50
USD_MIN_COLLATERAL = 1880

# THRESHOLDS - CLOSING
CLOSE_AT_ZSCORE_CROSS = True

# ETHEREUM ADDRESS
ETHEREUM_ADDRESS = "0x1E0984A857b56f00C730061B51D08e34289A569a"

# PRODUCTION KEYS
STARK_PRIVATE_KEY_MAINNET = config("STARK_PRIVATE_KEY_MAINNET")
DYDX_API_KEY_MAINNET = config("DYDX_API_KEY_MAINNET")
DYDX_API_SECRET_MAINNET = config("DYDX_API_SECRET_MAINNET")
DYDX_API_PASSPHRASE_MAINNET = config("DYDX_API_PASSPHRASE_MAINNET")

# DEVELOPMENT KEYS
STARK_PRIVATE_KEY_TESTNET = config("STARK_PRIVATE_KEY_TESTNET")
DYDX_API_KEY_TESTNET = config("DYDX_API_KEY_TESTNET")
DYDX_API_SECRET_TESTNET = config("DYDX_API_SECRET_TESTNET")
DYDX_API_PASSPHRASE_TESTNET = config("DYDX_API_PASSPHRASE_TESTNET")

# EXPORT KEYS
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_MAINNET if MODE == "PRODUCTION" else STARK_PRIVATE_KEY_TESTNET
DYDX_API_KEY = DYDX_API_KEY_MAINNET if MODE == "PRODUCTION" else DYDX_API_KEY_TESTNET
DYDX_API_SECRET = DYDX_API_SECRET_MAINNET if MODE == "PRODUCTION" else DYDX_API_SECRET_TESTNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_MAINNET if MODE == "PRODUCTION" else DYDX_API_PASSPHRASE_TESTNET

# EXPORT HOST
HOST = API_HOST_MAINNET if MODE == "PRODUCTION" else API_HOST_GOERLI

# HTTP PROVIDER
HTTP_PROVIDER_MAINNET = "https://eth-mainnet.g.alchemy.com/v2/kivDaob9_f96qtmsTlJ38s1pF3giNt8R"
HTTP_PROVIDER_TESTNET = "https://eth-goerli.g.alchemy.com/v2/Cml6zowW69d9Pv0DnBBGecQgKh0GLiic"
HTTP_PROVIDER = HTTP_PROVIDER_MAINNET if MODE == "PRODUCTION" else HTTP_PROVIDER_TESTNET