# coding=utf-8
import aip
import os
import asyncio
import argparse
import json

config = {
    "APP_ID": "17394652",
    "API_KEY": "EHUbRueuXyEaW2AGAn0cCXB3",
    "SECRETY_KEY": "0aGU9HdqqeXp76MV6GBB9wnMwAipRVR5"
}

client = aip.AipSpeech(
    config['APP_ID'], config['API_KEY'], config['SECRETY_KEY'])

options = {
    "per": 111
}


async def text2voice(txt):
    return client.synthesis(txt, options=options)


def make_data(data, sep="。\n"):
    return data.split(sep)


async def get_file_content(filename, c='utf8'):
    if not os.path.exists(filename) or not os.path.isfile(filename):
        print("文件不存在")
    try:
        sf = open(filename, 'r', encoding=c)
        data = sf.read()
        sf.close()
        return data
    except Exception as e:
        print(e)
        import sys
        sys.exit(1)


async def text2mp3str(data):
    ret = bytes()
    targetData = ""
    for item in data:
        if len(targetData) + len(item) <= 1024:
            targetData += item + "。"
        else:
            ret += await text2voice(targetData)
            targetData = ""

    if targetData != "":
        ret += await text2voice(targetData)

    return ret

