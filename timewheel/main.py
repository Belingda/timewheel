# coding=utf-8

from timewheel.misc import Log
import timewheel


def TestTick():
    Log("执行了定时任务")

def TestCallOut():
    timewheel.AddCallOut("test", 5, TestTick)

TestCallOut()
