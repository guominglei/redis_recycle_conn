# redis_recycle_conn
Python Redis客户端连接是一个长连接。
当项目实例多了以后。Redis服务器上的连接有可能会打满。或则有效利用率不高。
这时候Redis服务器就得做连接的timeout限制。来确保及时响应有效请求。

这时候，Python 对应的 Redis 客户端的连接池就不能满足要求了。
为何？连接发送消息时没有进行连接的有效性检验。即不知道此连接当前是否已经被服务器给啥死了。

本项目，在连接池里对连接进行了时间上的限制。再次使用时，如果超过指定时间，会先断开连接。然后重新连接。以确保连接的有效性。
