import tomllib

with open("config.toml", "rb") as f:
    data = tomllib.load(f)
    WOL_PORT = data['wol-port']
    HOST = data['server-host']
    TOKEN = data['discord-token']

with open('secret_key.bin', 'rb') as f:
    KEY = f.read()
