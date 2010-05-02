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
  def pushNewUser(self, mobno, password):
    sql = "INSERT INTO users VALUES( \"%s\",\"%s\")" % (mobno, password)
    print sql
    self.__cursor.execute(sql)
  def setNewPassword(self, mobno, password):
    sql = "UPDATE users SET password = \"%s\" where mobileno = \"%s\""
    self.__cursor.execute(sql % (password, mobno))
    if self.__cursor.rowcount==1:
      return True
    else:
      return False
  def isUserExists(self, mobno):
    sql = "SELECT * FROM users WHERE mobileno=\"%s\"" % mobno
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    if len(rows)==0:
      return False
    else:
      return True
  def isUserCorrect(self, mobno,passwd):
    sql = "SELECT * FROM users WHERE mobileno=\"%s\" and password=\"%s\"" % (mobno,passwd)
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    if len(rows)==0:
      return False
    else:
      return True
  def pushNewService(self, mobno, service, uid, password):
    sql = "SELECT * FROM accounts WHERE mobileno=\"%s\" and service=\"%s\"" % (mobno,service)
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    if len(rows)==0:
      sql = "INSERT INTO accounts VALUES( \"%s\",\"%s\", \"%s\", \"%s\")" % (mobno, service, uid, password)
      print sql
      self.__cursor.execute(sql)
    else:
      sql = "UPDATE accounts SET password = \"%s\", username=\"%s\" where mobileno = \"%s\" and service=\"%s\""
      print sql
      self.__cursor.execute(sql % (password, uid, mobno, service))
  def getAccount(self,mobno,service):
    sql = "SELECT username,password FROM accounts WHERE mobileno=\"%s\" and service=\"%s\"" % (mobno,service)
    self.__cursor.execute(sql)
    rows = self.__cursor.fetchall()
    if len(rows)==0:
      return None
    else:
      return rows[0]

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
