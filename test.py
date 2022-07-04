
from os import path
import json
from random import shuffle
from requests import get

# https://developer.oxforddictionaries.com/documentation


def call_thesaurus(word):
    base_url = "https://od-api.oxforddictionaries.com/api/v2"
    url = path.join(base_url, "thesaurus", "en-us", word.lower())

    r = get(url, headers = {"app_id":"1886dbb1",
                            "app_key":"b1d7dab86664ab89ec0b37b4765263e8",
                            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})

    print("code {}\n".format(r.status_code))
    print("text \n" + r.text)
    print("json \n" + json.dumps(r.json()))

    
    
    data = json.loads(r.content)
    print(data)

    """
    if "results" in data.keys():
        entries = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        thes_results = [entry["text"] for entry in entries]
        thes_results = [k for k in thes_results if " " not in k and "-" not in k]
        shuffle(thes_results)
    else:
        thes_results = []

    return(thes_results)
    """

call_thesaurus("zzz")