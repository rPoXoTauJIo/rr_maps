# --------------------------------------------------------------------------
# udp_server.py
#
# Description:
#
#   Simple udp socket server for testing
#   Will listen for udp messages and write them in listener_Hour_Minute_Seconds.log file
#
# Credits:
#   Simple udp socket server
#   Silver Moon (m00n.silv3r@gmail.com)
#
# -------------------------------------------------------------------------
global PREVIOUSFRAMELOCAL
global PREVIOUSFRAME
global LOGBUFFER

import socket
import sys
import time
import os
import math
from datetime import datetime

SERVERHOST = ''   # Symbolic name meaning all available interfaces
SERVERPORT = 8888  # Arbitrary non-privileged port
CURRENTCLIENT = None
startTime = time.time()
fileName = None

LOGBUFFER = []

PREVIOUSFRAME = 0.0
PREVIOUSFRAMELOCAL = 0.0


class StampObject:

    """
        Incapsulating stamp data received from external application
    """

    def __init__(self, position, rotation, timestamp, delta):
        self.position = position
        self.rotation = rotation
        self.timestamp = timestamp
        self.delta = delta

    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        return not self.timestamp == other.timestamp

    def __cmp__(self, other):
        if self.timestamp > other.timestamp:
            return 1
        elif self.timestamp < other.timestamp:
            return -1
        elif self.timestamp == other.timestamp:
            return 0

    def __hash__(self):
        return hash('timestamp', self.timestamp)


class Vector:
    """
        Class to incapsulate simple 3-dimensional logic
    """

    def __init__(self, stamp1, stamp2):
        self.x = 0
        self.y = 0
        self.z = 0
        self.initVector(stamp1, stamp2)

    def initVector(self, stamp1, stamp2):
        self.x = stamp1.position[0] - stamp2.position[0]
        self.y = stamp1.position[1] - stamp2.position[1]
        self.z = stamp1.position[2] - stamp2.position[2]


def processMessage(msg):

    processors = {
        'U_TIME': processUpdate,
        'U_POS_': processPosition,
        'U_ROT_': processRotation,
        'POSROT': processPositionAndRotation,

    }

    prefix = msg[0:6]
    if prefix in processors:
        reply = processors[prefix](msg.replace(prefix + ': ', ''))
    else:
        reply = msg
    if reply == None:
        return
    addMessageToBuffer(reply)
    print reply
    if len(LOGBUFFER) > 10:
        flushBuffer()


def processUpdate(msg):
    global MEANLIST

    delta = getDeltaFromUpdateMsg(msg)
    # print float.hex(delta)
    if len(MEANLIST) > 20:
        MEANLIST.append(abs(delta))
        del MEANLIST[0]
        mean = sum(MEANLIST) / float(len(MEANLIST))
    else:
        MEANLIST.append(delta)
        mean = 0.0
    newmsg = ''.join([''.join([msg.ljust(12, ' '), 'delta: %s' %
                               (delta)]).ljust(40, ' '), 'mean: %s' % (mean)])

    return newmsg


def processPosition(msg):
    # message = 'U_POS_[%s]'
    return msg.replace('POS', 'Position: ')


def processRotation(msg):
    # message = 'U_ROT_[%s]'
    return msg.replace('ROT', 'Rotation: ')


def processPositionAndRotation(msg):
    # message = 'POSROT: P%sP|R%sR|T(%s)T'
    positionString = msg[msg.find('P') + 2:msg.rfind('P')]
    rotationString = msg[msg.find('R') + 2:msg.rfind('R')]
    timeString = msg[msg.find('T') + 2:msg.rfind('T') - 1]
    deltaString = msg[msg.find('D') + 2:msg.rfind('D') - 1]

    posX = float(positionString[0:positionString.find(',')])
    posY = float(positionString[positionString.find(
        ',') + 1:positionString.rfind(',')])
    posZ = float(positionString[positionString.rfind(',') + 1:-1])
    position = (posX, posY, posZ)

    rotX = float(rotationString[0:rotationString.find(',')])
    rotY = float(rotationString[rotationString.find(
        ',') + 1:rotationString.rfind(',')])
    rotZ = float(rotationString[rotationString.rfind(',') + 1:-1])
    rotation = (rotX, rotY, rotZ)

    timeFloat = float(timeString)
    deltaFloat = float(deltaString)

    newStamp = StampObject(position, rotation, timeFloat, deltaFloat)

    reply = getFormattedReplyFromData(newStamp)
    #reply = getTurningAngles(newStamp)
    return reply


def getFormattedReplyFromData(stamp):
    reply = 'Position  : %s\nRotation  : %s\nTimestamp : %s\nDelta     : %s\n' % (
        str(stamp.position), str(stamp.rotation), str(stamp.timestamp), str(stamp.delta))
    return reply


def getTurningAngles(newStamp):
    global STAMPBUFFER

    STAMPBUFFER.append(newStamp)

    if len(STAMPBUFFER) < 3:  # cuz 2 vectors require 3 points
        return 'BUFFERING[%s]' % (len(STAMPBUFFER))

    while len(STAMPBUFFER) > 100:  # clearing so i wont run out of memory, premature optimization yes
        STAMPBUFFER.remove(min(STAMPBUFFER))

    STAMPLIST_INSTANT = getBorderValuesFromList(STAMPBUFFER, 3, 'max')
    iStamp1 = STAMPLIST_INSTANT[2]
    iStamp2 = STAMPLIST_INSTANT[1]
    iStamp3 = STAMPLIST_INSTANT[0]
    vectorAngle = (180.0 - math.degrees(getVectorAngle(iStamp1, iStamp2, iStamp3))
                   ) / (iStamp3.delta + iStamp2.delta + iStamp1.delta)  # reverse order
    reply = 'Angle  : %s' % (vectorAngle)
    return reply


def getInstantTurnAngle(stamp1, stamp2):

    diffYaw = stamp2.rotation[0] - stamp1.rotation[0]
    diffPitch = stamp2.rotation[1] - stamp1.rotation[1]
    diffRoll = stamp2.rotation[2] - stamp1.rotation[2]

    return (diffYaw, diffPitch, diffRoll)


def getVectorAngle(stamp1, stamp2, stamp3):
    # {A.x - B.x, A.y - B.y, A.z - B.z} - vector1
    # {C.x - B.x, C.y - B.y, C.z - B.z} - vector2
    vector1 = (stamp1.position[0] - stamp2.position[0], stamp1.position[
               1] - stamp2.position[1], stamp1.position[2] - stamp2.position[2])
    vector2 = (stamp3.position[0] - stamp2.position[0], stamp3.position[
               1] - stamp2.position[1], stamp3.position[2] - stamp2.position[2])

    # normalization of first vector
    # sqrt(v1.x * v1.x + v1.y * v1.y + v1.z * v1.z)
    # {v1.x / v1mag, v1.y / v1mag, v1.z / v1mag}
    vector1magnitude = math.sqrt(
        vector1[0] * vector1[0] + vector1[1] * vector1[1] + vector1[2] * vector1[2])
    if vector1magnitude == 0:
        return 0.0
    vector1normalized = (vector1[0] / vector1magnitude, vector1[1] /
                         vector1magnitude, vector1[2] / vector1magnitude)

    # nomalization of second vector
    # sqrt(v2.x * v2.x + v2.y * v2.y + v2.z * v2.z)
    # {v2.x / v2mag, v2.y / v2mag, v2.z / v2mag}
    vector2magnitude = math.sqrt(
        vector2[0] * vector2[0] + vector2[1] * vector2[1] + vector2[2] * vector2[2])
    if vector2magnitude == 0:
        return 0.0
    vector2normalized = (vector2[0] / vector2magnitude, vector2[1] /
                         vector2magnitude, vector2[2] / vector2magnitude)

    # calculating dot product
    # v1norm.x * v2norm.x + v1norm.y * v2norm.y + v1norm.z * v2norm.z
    dotProduct = (vector2normalized[0] * vector1normalized[0] + vector2normalized[
                  1] * vector1normalized[1] + vector2normalized[2] * vector1normalized[2])

    angle = math.acos(dotProduct)

    # returning angle in radians
    return angle


def getBorderValuesFromList(initial_list, num=3, order='max'):

    newlist = []
    old_list = list(initial_list)
    for i in xrange(0, num):
        if order == 'max':
            value = max(old_list)
        elif order == 'min':
            value = min(old_list)

        newlist.append(value)
        old_list.remove(value)

    return newlist


def compareTime(time1, time2):
    try:
        diff = time1 - time2
    except:
        diff = 0.0
    return diff


def getDeltaFromUpdateMsg(msg):
    global PREVIOUSFRAME
    global PREVIOUSFRAMELOCAL

    filteredTime = float()
    expectedTime = expectTime() + PREVIOUSFRAME
    delta = compareTime(filteredTime, expectedTime)
    PREVIOUSFRAME = filteredTime
    PREVIOUSFRAMELOCAL = time.time()
    return delta


def expectTime():
    expectedTime = time.time() - PREVIOUSFRAMELOCAL
    # print 'EXPECT: ' + str(expectedTime)
    return expectedTime


def setFilename():
    global fileName

    if fileName != None and os.path.isfile(fileName):
        os.remove(fileName)
    fileName = 'listener2_%s_%s.log' % (
        datetime.now().hour, datetime.now().minute)


def writeMessage(msg):
    try:
        logFile = open(fileName, 'a')
        logFile.write(str(msg) + '\n')
        logFile.close()
    except:
        print 'failed to write log msg at %s' % (time.time())


def addMessageToBuffer(msg):
    global LOGBUFFER

    LOGBUFFER.append(msg)


def flushBuffer():
    global LOGBUFFER

    # try:
    logFile = open(fileName, 'a')
    for msg in LOGBUFFER:
        logFile.write(str(LOGBUFFER.pop(-1)) + '\n')
    logFile.close()
    # except:
    #    print 'failed to flush buffer at %s to %s' % (time.time(), fileName)


# Datagram (udp) socket
try:
    S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


# Bind socket to local host and port
try:
    S.bind((SERVERHOST, SERVERPORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'
setFilename()

# now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = S.recvfrom(1024)
    data = d[0]  # data
    addr = d[1]  # ip and port

    if data == 'LISTEN':
        setFilename()
        startTime = time.time()
        print 'STARTED LISTENER'
        continue

    if CURRENTCLIENT != (addr[0]):
        CURRENTCLIENT = (addr[0])
        print 'Message from[%s:%s]' % (addr[0], addr[1])

    processMessage(data)

S.close()
