## Installation

Check your validator_address:
```bash
curl -s localhost:26657/status | jq .result.validator_info.address
```

Create your config file from sample:
```bash
cp config-sample.yml config.yml
```

Paste your node info in `watchlist` section in `config.yml`.

Paste your telegram bot url and chat id in `telegram` section in `config.yml`.


## Usage

```bash
python check_missed_blocks.py --help
```