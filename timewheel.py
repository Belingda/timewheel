# coding=utf-8
from misc import *

import threading

'''
版本1：时钟驱动方式 每N间隔时间驱动一次
当前在第几个时间轮
上层时间轮结构：
[[],[]]
第二层时间轮：
[当前在第几个时间槽,[(过期时间,任务key),(过期时间,任务key),]]
底层时间轮结构
[[任务key1，任务key2],[]]

对外接口
def CallOut() # 添加任务
def RemoveCallOut() # 删除任务
'''

TIMESLOT_LIMIT = 3
import time
class TimeManager(object):
	def __init__(self):
		self.m_CurTimeWheelsIndex = 0	#当前在第几个时间轮
		self.m_BottomTimeSlot = [[] for i in range(TIMESLOT_LIMIT)]	# 最底层时间轮
		self.m_TimeWheels = [[0,[[] for j in range(TIMESLOT_LIMIT)]] for i in range(TIMESLOT_LIMIT)]		# 上层时间轮
		self.m_BottomCursor = 0		# 底层时间轮游标
		self.m_TaskKey2CallBackFunc = {}

	def StartTick(self):
		while(True):
			self.DealTask()
			self.m_BottomCursor += 1
			if self.m_BottomCursor == TIMESLOT_LIMIT:
				self.m_BottomCursor = 0
				self.MoveTimeWheelsTaskToBottom()
			time.sleep(1)

	def AddTaskCallOut(self, taskkey, delayseconds, func, *args):
		timewheelindex = (self.m_BottomCursor + delayseconds) // TIMESLOT_LIMIT
		if timewheelindex <= 0: # 直接加入最底层时间轮
			slotindex = (self.m_BottomCursor + delayseconds) % TIMESLOT_LIMIT - 1
			self.m_BottomTimeSlot[slotindex].append(taskkey)
			self.m_TaskKey2CallBackFunc[taskkey] = (func, args)
		else: # 两层时间轮情形下
			slotindex = (self.m_BottomCursor + delayseconds) // TIMESLOT_LIMIT - 1
			recorddelay = (self.m_BottomCursor + delayseconds) % TIMESLOT_LIMIT
			self.m_TimeWheels[timewheelindex-1][1][slotindex].append((recorddelay, taskkey))
			Log("加定时任务 {0} {1} {2}".format(self.m_BottomCursor, recorddelay, self.m_TimeWheels[timewheelindex-1]))
		Log("加定时任务 {0}".format(self.m_TimeWheels[0]))

	def MoveTimeWheelsTaskToBottom(self):
		# [当前在第几个时间槽, [[(过期时间, 任务key),()],[(过期时间)] ]  ]
		nowslotindex, alltasklst = self.m_TimeWheels[0] # 上层时间轮 （第二层）
		taskls = alltasklst[nowslotindex]
		for task in taskls:
			delay, taskkey = task
			self.m_BottomTimeSlot[delay].append(taskkey)
		self.m_TimeWheels[0][0] += 1
		Log("MoveTimeWheelsTaskToBottom m_TimeWheels {0}".format(self.m_TimeWheels[0]))
		Log("MoveTimeWheelsTaskToBottom m_BottomTimeSlot{0}".format(self.m_BottomTimeSlot))

	def DealTask(self):
		tasklst = self.m_BottomTimeSlot[self.m_BottomCursor]
		for taskkey in tasklst:
			func, args = self.m_TaskKey2CallBackFunc[taskkey]
			func(args) if args else func()
			del self.m_TaskKey2CallBackFunc[taskkey]
		self.m_BottomTimeSlot[self.m_BottomCursor] = []

timemanager = TimeManager()

def AddCallOut(taskkey, delayseconds, func, *args):
	p = threading.Thread(target = timemanager.AddTaskCallOut,args=(taskkey, delayseconds, func, *args))
	p.start()

def StartTick():
	p = threading.Thread(target=timemanager.StartTick)
	p.start()
	Log("时钟开始驱动")

StartTick()
