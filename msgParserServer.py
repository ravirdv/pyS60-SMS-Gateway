# -*- coding: utf-8 -*-
from SMS import SMS
import lightblue, threading, MySQLdb, time
from db import database


class SenderThread (threading.Thread):
  def __init__ ( self ):
    threading.Thread.__init__ ( self )
  def run ( self ):
    sendSkt = lightblue.socket()
    sendSkt.bind(("", 0))  
    sendSkt.listen(1)
    lightblue.advertise("SMS Gateway (Response Thread)", sendSkt, lightblue.RFCOMM)
    db = database()
    conn2, addr2 = sendSkt.accept()
    print "Connected to Response Server", addr2
    while 1:
      time.sleep(1)
      db= database()
      rows = db.popOutboxMsg()
      for row in rows:
	print "Sending Msg -> %s" % (row[0])
	sms=SMS(str(row[0]), row[1],row[2], row[3], str(row[4]))
        toSend = sms.toXML()
	print toSend
        conn2.send(toSend.replace("\n","\\n"))
        res = conn2.recv(1024)
        print res
        while (res != "1" and res != "2"):
	  res = conn2.recv(1024)
	  print res
        db.setOutboxProcessed(str(row[0]), res) 


class ReceiverThread (threading.Thread):
  def __init__ ( self ):
    threading.Thread.__init__ ( self )
  
  def run ( self ):
    s = lightblue.socket()
    s.bind(("", 0))
    s.listen(2)
    lightblue.advertise("SMS Gateway (Request Thread)", s, lightblue.RFCOMM) 
    conn, addr = s.accept()
    print "Connected to Request Server", addr
    while 1:
      resp = conn.recv(1024)
      print resp
      msg = SMS(resp)
      db = database()
      db.pushInboxMsg(msg.id, msg.to, msg.frm, msg.text, msg.timestamp)
    conn.close()
    s.close() 
      
SenderThread().start()
ReceiverThread().start()
print "Server up, waiting for client"
