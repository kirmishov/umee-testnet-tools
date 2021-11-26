import itertools
import requests
import yaml


with open('config.yml', 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)


validators_status_lst = config['watchlist']
for v in validators_status_lst:
    v['jailed'] = None
    v['missed_blocks'] = []


def check_missed_block(validators_status_lst, block_height):
    for v in validators_status_lst:
        data = request_get(f'http://{config["rpc"]}/block?height={block_height}')
        if not any(d['validator_address'] == v['validator_address'] for d in data['result']['block']['last_commit']['signatures']):
            sendMessage(f'{v["name"]} missed block: {block_height} | timestamp: {data["result"]["block"]["header"]["time"]}')
            v['missed_blocks'].append(block_height)


def check_is_jailed(validators_status_lst):
    for v in validators_status_lst:
        data = request_get(f'http://{config["rest"]}/staking/validators/{v["valoper"]}')
        last_status = data["result"]["jailed"]
        if v['jailed'] != last_status:
            sendMessage(f'{v["name"]} jailed: {last_status}')
            v['jailed'] = last_status


def request_get(url, attempts = 3):
    r = None
    i = 0
    while (r is None and i < attempts):
        try:
            i+=1
            r = requests.get(url)
            return r.json()
        except Exception as e:
            print(e, url)


def sendMessage(text):
    try:
        r = requests.post(url = config['telegram']['send_message_url'], data = {'chat_id': config['telegram']['chat_id'], 'text': text})
    except:
        print(f'Unsuccessful attempt send message: {text}')


if __name__ == '__main__':
    for block_height in itertools.count(start=1):
        check_is_jailed(validators_status_lst)
        check_missed_block(validators_status_lst, block_height)