import requests
import os
import json

# DOCS: https://api.imgflip.com/

dirpath = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(dirpath, "configs")
meme_conf_name = os.path.join(config_dir, "meme_conf.json")

os.makedirs(config_dir, exist_ok=True)

# Method: GET
template_url = "https://api.imgflip.com/get_memes"

# Method: POST
generate_url = "https://api.imgflip.com/caption_image"

def meme(message):
    data = parse_message(message)
    print(data)
    if data:
        conf = get_conf()
        uname, pw = conf['username'], conf['password']
        if uname is not '' and pw is not '':
            return generate_meme(data['template'], uname, pw, data['top'], data['bot']) 
        else:
            return "Meme is unconfigured. Check logs."
    else:
        return "Invalid format, correct: !meme [memeId nameId]; [(optional) text1]; [(optional) text2]\n"\
               "For meme ids check here: https://api.imgflip.com/popular_meme_ids"

def generate_meme(template_id, username, password, top_text, bot_text):
    body = {
        'template_id': template_id,
        'username': username,
        'password': password,
        'text0': top_text,
        'text1': bot_text
    }
    try:
        r = requests.post(generate_url, data=body)
        resp = r.json()
        if resp['success']:
            return resp['data']['url']
        else:
            return resp['error_message']
    except Exception as e:
        print("Error fetching meme.", e)
        return 'Ooops..something went wrong.'

def parse_message(message):
    """
    !meme [meme name]; [(optional) text1]; [(optional) text2]
    """
    args = []
    template, top, bot = '', '', ''
    try:
        args = message.split('!meme')[1].split(';')
        print(args)
        cnt = len(args)    
        if cnt >= 1:
            template = args[0].lstrip().split(' ')[0]
        if cnt >= 1:
            top = args[0].lstrip().split(' ')[1]
        if cnt >= 2:
            bot = args[1]
        return {'template': template, 'top': top, 'bot': bot}
    except Exception as e:
        print("Error parsing message.", e)
        return False

def get_conf():
    try:
        default = {"username": '', 'password': ''}
        if os.path.isfile(meme_conf_name):
            with open(meme_conf_name) as conf:
                return json.load(conf)
        else:
            with open(meme_conf_name, "w+") as conf:
                json.dump(default, conf)
                print("Created new config: ", meme_conf_name)
            return default
    except Exception as e:
        print("Error handling config.", e)
        return default
        
get_conf()