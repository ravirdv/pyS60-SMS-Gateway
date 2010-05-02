# -*- coding: utf-8 -*-
import inbox, e32, lightblue, threading, messaging, time, sys, appuifw
from xml.dom import minidom, Node
class SMS:
  def __init__(self, str, to=None, frm=None, txt=None, ts=None):
    if to==None:
      self.xml=str
      doc = minidom.parseString(str)
      node = doc.documentElement
      if node.nodeType == Node.ELEMENT_NODE:
	for (name, value) in node.attributes.items():
	  if name.lower()=="id":
	    self.id=value
	  if name.lower()=="to":
	    self.to=value
	  if name.lower()=="from":
	    self.frm=value
	  if name.lower()=="sms":
	    self.text=value
	  if name.lower()=="timestamp":
	    self.timestamp=value
    else:
      self.id=str
      self.to=to
      self.frm=frm
      self.text=txt
      self.timestamp=ts
      self.xml ='<?xml version="1.0"?><message'
      self.xml = self.xml + ' id = \"' + self.id + '\"'
      self.xml = self.xml + ' to = \"' + self.to + '\"'
      self.xml = self.xml + ' from = \"' + self.frm + '\"'
      self.xml = self.xml + ' sms =\"' + self.text + '\"' 
      self.xml = self.xml + ' timestamp =\"' + self.timestamp + '\"'
      self.xml = self.xml + '></message>'
  def toXML(self):
    return self.xml

  def __str__(self):
    return "To\t: %s\nFrom\t: %s\nText\t: %s\nTime\t: %s" % (self.to, self.frm, self.text, self.timestamp)


class SenderThread (threading.Thread):
  def __init__ ( self ):
    threading.Thread.__init__ ( self )
  def cb(self,state):
    if state ==messaging.ESent:
      self.rcvSkt.send("1")
    if state==messaging.ESendFailed:
      self.rcvSkt.send("FAILED")
      outbox = inbox.Inbox(inbox.EOutbox)
      if outbox.sms_messages() is not None:
	for m in outbox.sms_messages():
	  outbox.delete(m)
      self.rcvSkt.send("2")
    #if state ==messaging.EFatalServerError:
    #  self.rcvSkt.send("Probably No Coverage, no simcard or service has beed suspended by your provider, can't help dude :) ")
    #if state ==messaging.EDeleted:
    #  self.rcvSkt.send("NAK")
      
  def run ( self ):
    self.rcvSkt = lightblue.socket()
    self.rcvSkt.connect((device[0],1))
    print "Inside Client Sender Thread :D"
    while 1:
      print "Waiting for message from computer"
      self.response = self.rcvSkt.recv(1024)
      sms=SMS(self.response)
      print sms.to + sms.text
      messaging.sms_send(sms.to, sms.text, "7bit", self.cb)
      

class ReceiverThread(threading.Thread):
  def __init__ ( self ):
     threading.Thread.__init__ ( self )
  def callback(self,id):
    box=inbox.Inbox()
    #if id in box.sms_messages():
    sms=SMS(str(id), "9033588066", box.address(id), box.content(id), str(box.time(id)))
    toSend = sms.toXML()
    self.sndSkt.send(toSend)
    box.delete(id)
  def run ( self ):
    print "Inside Client receiver Thread :D"
    self.sndSkt = lightblue.socket()
    self.sndSkt.connect((device[0],2))
    box=inbox.Inbox()
    box.bind(self.callback)
    app_lock = e32.Ao_lock()
    app_lock.wait()
    self.sndSkt.close()

device = lightblue.selectdevice()
print device[0]
ReceiverThread().start()
SenderThread().start()
print "Waiting for new SMS messages.."
app_lock = e32.Ao_lock()
app_lock.wait()
