#!/usr/local/env python
# -*- coding: utf-8 -*-

"""
    Author: GuoMingLei
    Created: 2019/5/13

   redis 现有的pool socket链接是长链接。
   如果Redis服务器端对socket 链接进行休眠链接清理。
   那么socket链接就会出现问题。

   解决方案是：
   1、connection 对象添加最后使用时间.
   2、pool 初始化时，添加参数用于标记回收时间。 pool_recycle=60 秒
   3、pool  get_connection 方法是添加检查空闲时间逻辑
   4、pool release 方法添加本次是否时间逻辑。
"""
import time
from redis.connection import Connection, ConnectionPool


class ConnectionLastest(Connection):

    def __init__(self, **kwargs):

        super(ConnectionLastest, self).__init__(**kwargs)

        # 添加最后释放时间 单位秒
        self.release_tm = 0


class ConnectionRecyclePool(ConnectionPool):

    def __init__(self,
                 connection_class=ConnectionLastest,
                 max_connections=None,
                 pool_recycle=60,
                 **connection_kwargs):
        """
            重写初始化方法。
            1、替换connection_class
            2、添加pool_recycle参数用于检查空闲时间 注意要小于服务器设置的时间
        """
        print pool_recycle
        max_connections = max_connections or 2 ** 31
        if not isinstance(max_connections, (int, long)) or max_connections < 0:
            raise ValueError('"max_connections" must be a positive integer')

        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.max_connections = max_connections
        self.pool_recycle = pool_recycle
        self.reset()

    def get_connection(self, command_name, *keys, **options):
        """
            重写获取连接
            添加检查release_tm逻辑
        """
        self._checkpid()
        try:
            connection = self._available_connections.pop()
            now = time.time()
            # 添加 检测上次释放时间。如果空闲时间达到阀值。就断开连接重新连接
            if (now - connection.release_tm) > self.pool_recycle:
                connection.disconnect()
                connection.connect()

        except IndexError:
            connection = self.make_connection()
        self._in_use_connections.add(connection)
        return connection


    def release(self, connection):
        "Releases the connection back to the pool"
        self._checkpid()
        if connection.pid != self.pid:
            return

        # 添加释放时间
        connection.release_tm = int(time.time())

        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)