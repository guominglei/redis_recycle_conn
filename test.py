#!/usr/local/env python
# -*- coding: utf-8 -*-

"""
    Author: GuoMingLei
    Created: 2019/5/13
   
"""
import time
import redis
from recycle_connection import ConnectionRecyclePool


config = "redis://:@127.0.0.1:6379/0"
client = redis.Redis(connection_pool=ConnectionRecyclePool.from_url(config, pool_recycle=10))


def test():

    info = client.get("actopus_audio2txt_switch")
    print info
    time.sleep(60)
    client.set("actopus_audio2txt_switch", "2")
    info = client.get("actopus_audio2txt_switch")
    print info


if __name__ == "__main__":

    test()
