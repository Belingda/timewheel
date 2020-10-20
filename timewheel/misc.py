# coding=utf-8
import time
def Log(txt):
	timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print("{0}{1}".format(timestr,txt))