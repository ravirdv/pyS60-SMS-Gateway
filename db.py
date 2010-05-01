# -*- coding: utf-8 -*-
import  MySQLdb
from datetime import datetime
from time import time
class database:
  def __init__(self):
    self.__DB = MySQLdb.connect(host="localhost", user="root", passwd="new-password",db="smsgw")
    self.__cursor = self.__DB.cursor()
  def pushOutboxMsg(self, sms_to, sms_text):
    t=time()
    sms_text=sms_text.replace("@gmail.com", "")
    sql = "INSERT INTO outbox VALUES( NULL ,\"%s\",\"%s\" , \"%s\", \"%s\", %d )" % (sms_to, "+919033588066", sms_text, datetime.fromtimestamp(t), 0)
    print sql
    self.__cursor.execute(sql)
  def pushInboxMsg(self, msg_id, sms_to, sms_from, sms_text, sms_timestamp):
    #t=time()
    #sms_text=sms_text.replace("@gmail.com", "")
    sql = "INSERT INTO inbox VALUES( %d ,\"%s\",\"%s\" , \"%s\", \"%s\", %d )" % ( int(msg_id),sms_to, sms_from, sms_text, datetime.fromtimestamp(float(sms_timestamp)), 0)
    print sql
    self.__cursor.execute(sql)
  def popInboxMsg(self):
    sql = "SELECT * FROM inbox WHERE processed = 0"
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    return rows
  def popOutboxMsg(self):
    sql = "SELECT * FROM outbox WHERE processed = 0"
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    return rows
  def setInboxProcessed(self, msg_id, status):
    sql = "Update inbox set processed = %s where id = %s"
    print sql % (status, msg_id)
    self.__cursor.execute(sql % (status, msg_id))
  def setOutboxProcessed(self, msg_id, status):
    sql = "UPDATE outbox SET processed = %s where id = %s"
    self.__cursor.execute(sql % (status, msg_id))

def Hash(key):
   BitsInUnsignedInt = 1 * 8
   ThreeQuarters     = long((BitsInUnsignedInt  * 3) / 4)
   OneEighth         = long(BitsInUnsignedInt / 8)
   HighBits          = (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
   hash              = 0
   test              = 0

   for i in range(len(key)):
     hash = (hash << OneEighth) + ord(key[i])
     test = hash & HighBits
     if test != 0:
       hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));
   return (hash & 0x7FFFFFFF)
