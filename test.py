
from email.mime import base
from os import path
from json import loads
from logging import info
from random import choice, shuffle
from requests import get, Session

# https://developer.oxforddictionaries.com/documentation


def call_lemma(tag: str, base_url: str, session):
    url = path.join(base_url, "lemmas", "en-us", tag)
    data = loads(
        session.get(url).content
    )

    if "results" in data.keys():
        lemm_results = data['results'][0]['lexicalEntries'][0]['inflectionOf'][0]['text']
    else:
        lemm_results = tag
    return(lemm_results)


def call_thesaurus(tag: str, base_url: str, session):
    url = path.join(base_url, "thesaurus", "en-us", tag)
    data = loads(
        session.get(url).content
    )

    if "results" in data.keys():
        entries = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        thes_results = [entry["text"] for entry in entries]
        thes_results = [k for k in thes_results if " " not in k and "-" not in k]
        shuffle(thes_results)
    else:
        thes_results = []

    return(set(thes_results))


def search_oxford(tag: str, tagSet: set):
    base_url = "https://od-api.oxforddictionaries.com/api/v2"
    headers = {"app_id":"1886dbb1",
               "app_key":"b1d7dab86664ab89ec0b37b4765263e8"}

    # Start requests session
    session = Session()
    session.headers.update(headers)

    # Call lemma
    lemm_tag = call_lemma(tag = tag, base_url = base_url,
                          session = session)

    # Possibly call thesaurus
    if lemm_tag not in tagSet:

        try:
            thes_results = call_thesaurus(tag = lemm_tag, 
                                          base_url = base_url,
                                          session = session)
            thes_matches = thes_results.intersection(tagSet)
            ox_result = choice(tuple(thes_matches))
        except IndexError:
            ox_result = None
    else:
        ox_result = lemm_tag

    # Return Result    
    return(ox_result)


tagSet = set( ["worried", "run", "duck"] )

while True:
    tag = input("input: ")
    ox_results = search_oxford(tag, tagSet)
    print(ox_results)