## Installation

Check your validator_address:
```bash
curl -s localhost:26657/status | jq .result.validator_info.address
```


```bash
cp config-sample.yml config.yml
```

Paste your node info in `watchlist` section in `config.yml`.

Paste your telegram bot url and chat id in `telegram` section in `config.yml`.

