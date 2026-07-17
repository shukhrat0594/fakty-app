#!/usr/bin/env python3
import json
import os
import random
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, '..', 'data.js')

CAT_EMOJI = {
    'Рандом': '🎲', 'История': '🏛', 'Литература': '📖', 'Цитаты': '💬',
    'Науки': '🔬', 'Шекспир': '🎭', 'Греки': '🏺', 'Христианство': '✝️',
    'Искусство': '🎨', 'Спорт': '⚽', 'Перифразы': '🏷', 'Прототипы': '🕵️',
    'Псевдонимы': '🎩', 'Имена разных стран': '🌍', 'Олимпийские игры': '🥇',
    'Нобелевские лауреаты': '🏅', 'Латинские выражения': '🏛️',
}


def load_data():
    text = open(DATA_PATH, encoding='utf-8').read().strip()
    text = re.sub(r'^const DATA\s*=\s*', '', text)
    text = re.sub(r';\s*$', '', text)
    return json.loads(text)


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_message(item):
    emoji = CAT_EMOJI.get(item['cat'], '💡')
    lines = [f"{emoji} <b>{esc(item['cat'])}</b>", '']
    if 'q' in item:
        lines.append(f"❓ <b>{esc(item['q'])}</b>")
        lines.append(f"👉 {esc(item['a'])}")
        if item.get('note'):
            lines.append('')
            lines.append(f"<i>{esc(item['note'])}</i>")
    elif item.get('term'):
        lines.append(f"<b>{esc(item['term'])}</b>")
        lines.append(esc(item['def']))
    else:
        lines.append(esc(item['text']))
    return '\n'.join(lines)


def send(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = json.dumps({
        'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML',
        'disable_web_page_preview': True,
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
        print(body)
        if not json.loads(body).get('ok'):
            raise SystemExit(1)


def main():
    token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    data = load_data()
    item = random.choice(data['pairs'] + data['facts'])
    send(token, chat_id, build_message(item))


if __name__ == '__main__':
    main()
