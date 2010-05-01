# -*- coding: utf-8 -*-
import inbox, e32, lightblue, threading, messaging

class SenderThread (threading.Thread):
  def __init__ ( self ):
    rcvSkt = lightblue.socket()
    rcvSkt.connect(("11:11:11:11:11:11",2))
  def run ( self ):
    print "Inside Client Sender Thread :D"
    while 1:
      response = rscSkt.recv(1024)
       #messaging.sms_send(self.no, response)     
      print response

class ReceiverThread(threading.Thread):
  def __init__ ( self ):
    sndSkt = lightblue.socket()
    sndSkt.connect(("11:11:11:11:11:11",1))
    
  def callback(id):
    box=inbox.Inbox()
    toSend ='<?xml version="1.0"?><message'
    toSend = toSend + ' id = \"' + str(id) + '\"'
    toSend = toSend + ' to = \"9033588066\"'
    toSend = toSend + ' from = \"' + box.address(id) + '\"'
    toSend = toSend + ' sms =\"' + box.content(id) + '\"' 
    toSend = toSend + ' time =\"' + str(box.time(id)) + '\"'
    toSend = toSend + '</message>'
    sndSkt.send(toSend)   
  def run ( self ):
    print "Inside Client receiver Thread :D"
    sndSkt = lightblue.socket()
    sndSkt.connect(("11:11:11:11:11:11",1))
    box=inbox.Inbox()
    box.bind(self.callback)
    app_lock = e32.Ao_lock()
    app_lock.wait()
    sndSkt.close()
  
SenderThread().start()
ReceiverThread().start()
print "Waiting for new SMS messages.."
app_lock = e32.Ao_lock()
app_lock.wait()
sndSkt.close()
