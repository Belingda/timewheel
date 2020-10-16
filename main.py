# coding=utf-8

from misc import Log
import threading
import timewheel
import time

def TestTick():
    Log("执行了定时任务")

def TestCallOut():
    timewheel.AddCallOut("test", 5, TestTick)

TestCallOut()
