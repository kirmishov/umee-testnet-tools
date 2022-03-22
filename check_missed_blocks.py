import itertools
import argparse
import requests
import yaml


with open('config.yml', 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)


validators_status_lst = config['watchlist']
for v in validators_status_lst:
    v['jailed'] = None
    v['missed_blocks'] = []


def check_missed_block(validators_status_lst, block_height):
    try:
        for v in validators_status_lst:
            data = request_get(f'{config["rpc"]}/block?height={block_height}')
            if not any(d['validator_address'] == v['validator_address'] for d in data['result']['block']['last_commit']['signatures']):
                sendMessage(f'{v["name"]} missed block: {block_height} | timestamp: {data["result"]["block"]["header"]["time"]}')
                v['missed_blocks'].append(block_height)
        return validators_status_lst
    except:
        # case if block_height higher than the current blockchain height
        return None


def check_is_jailed(validators_status_lst):
    try:
        for v in validators_status_lst:
            data = request_get(f'{config["rest"]}/staking/validators/{v["valoper"]}')
            last_status = data["result"]["jailed"]
            if v['jailed'] != last_status:
                sendMessage(f'{v["name"]} jailed: {last_status}')
                v['jailed'] = last_status
    except:
        pass


def request_get(url, attempts = 3):
    r = None
    i = 0
    while (r is None and i < attempts):
        try:
            i+=1
            print(url)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start_block_height", type=int, default=1)
    args = parser.parse_args()

    for block_height in itertools.count(start=args.start_block_height):
        check_is_jailed(validators_status_lst)
        validators_status_actual = check_missed_block(validators_status_lst, block_height)
        while not validators_status_actual:
            validators_status_actual = check_missed_block(validators_status_lst, block_height)