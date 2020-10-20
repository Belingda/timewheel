# coding=utf-8
'''
插入（更新）排行榜 ZADD key score member
根据id查询名次  zrank key member
根据名次查询id  zrank key low high (返回第high名)
查询前N zrange key 0 N
整个榜单 zrange key 0 -1
top k
all
zrevrank 从大到小
zrank 从小到大

zhash {id:信息}
'''

import time
import redis
import json
import random
g_RedisConn = None

def GetRedisConn(): # 这里需要一个单例
	global g_RedisConn
	if not g_RedisConn:
		pool = redis.ConnectionPool(host='localhost', port=6379)
		g_RedisConn = redis.Redis(connection_pool=pool)
	return g_RedisConn

class redisconn(object):
	def __init__(self):
		pass

class rank(object):
	def __init__(self,rankname):
		self.m_RankName = rankname

	def InsertRank(self, pid, score, *args):
		args = json.dumps(args)
		r = GetRedisConn()
		r.zadd(self.m_RankName + "score", {pid:score})
		r.hset(self.m_RankName + "info", pid, args)

	def GetInfoByRankNum(self,ranknum):
		r = GetRedisConn()
		pid = r.zrange(self.m_RankName + "score",ranknum-1,ranknum-1)
		if not pid:
			return []
		pinfo = r.hget(self.m_RankName + "info",key=pid[0])
		return json.loads(pinfo)

def TestFunc():
	rob = rank("testrank")
	testdata = [(10000000, 100, 100) for i in range(100000)]
	print("开始计时")
	st = time.clock()
	rob.GetInfoByRankNum(10)
	print(time.clock() - st)


TestFunc()






