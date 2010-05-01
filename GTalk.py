# -*- coding: utf-8 -*-
import xmpp
import time
import threading
from db import database,Hash
class GTalk(threading.Thread):
  
  def __init__ (self, mobno):
    self.L={}
    self.mobno=mobno
    self.killed=False
    threading.Thread.__init__ (self)

  def __presenceHandler(self,conn,presence_node):
	  if presence_node.getFrom()!=None:
		  print "%s : %s/%s" % (self.mobno, Hash(presence_node.getFrom().getStripped()), presence_node.getFrom().getStripped())
		  #if presence_node.getStatus()!=None:
			  #print "Status : " + presence_node.getStatus()
		  if presence_node.getFrom().getResource()!=None and len(presence_node.getFrom().getResource())>5:
			  #print "Online on : " + presence_node.getFrom().getResource()
			  if not str(presence_node.getFrom().getStripped()) in self.L:
			    self.L[str(Hash(presence_node.getFrom().getStripped()))]=presence_node.getFrom().getStripped()
		  else:
		    if str(Hash(presence_node.getFrom().getStripped())) in self.L: #if user is offine or inivisble
		      del self.L[str(Hash(presence_node.getFrom().getStripped()))]
		  #if presence_node.getPriority()!=None:
			#  print "Priority : " + presence_node.getPriority()
		  #if presence_node.getShow()!=None:
			 # print "Show : " + presence_node.getShow()
		  #if presence_node.getNick()!=None:
			#  print "Nick : " + presence_node.getNick()

  def __iqHandler(self,conn,iq_node):
	  reply=iq_node.buildReply('result')
	  conn.send(reply)
	  #raise NodeProcessed

  def __messageHandler(self,conn,mess_node):
	  #reply=mess_node.buildReply(mess_node.getFrom().getStripped() + " is online on " + mess_node.getFrom().getResource())
	  #print "Reply sent to " +  mess_node.getFrom().getStripped() + " !!!"
	  if mess_node.getBody()!=None:
	    if not str(mess_node.getFrom().getStripped()) in self.L:
	      self.L[str(Hash(mess_node.getFrom().getStripped()))]=mess_node.getFrom().getStripped()
	    db = database()
	    db.pushOutboxMsg(self.mobno, "G%d/%s:%s" % (Hash(mess_node.getFrom().getStripped()),mess_node.getFrom().getStripped(),mess_node.getBody()))
	    print "Message : " + mess_node.getBody()
	  #conn.send(reply)

  def connect(self, user, password):
    self.client = xmpp.Client('gmail.com')
    print "Connecting..."
    self.client.connect(server=('talk.google.com', 5223))
    print "Connected!"
    print "Authenticating..."
    if self.client.auth(user, password, resource='Vishal_Personal_Bot', ) is None:
      print "Login failed"
      return False
    print "Authenticated!"
    self.client.RegisterHandler('presence',self.__presenceHandler)
    self.client.RegisterHandler('iq',self.__iqHandler)
    self.client.RegisterHandler('message',self.__messageHandler)
    self.client.sendInitPresence()
    print "Inital Presence sent!"
    return True
    
  def run(self):
    while True and not self.killed:
      if not self.client.isConnected():
	self.client.reconnectAndReauth()
      self.client.Process(1)
  
  def getOnlineUsers(self):
    return self.L
  
  def disconnect(self):
    self.killed=True
    self.client.disconnect()

  def sendImFromId(self,emailhash, msg):
    if emailhash in self.L:
      self.sendImFromEmail(self.L[emailhash],msg)
      return True
    else:
      return False

  def sendImFromEmail(self,email,msg):
    self.client.send( xmpp.Message(email, msg))
    print "Message sent!\n"
	    #if not self.client.isConnected():
		#    self.client.reconnectAndReauth()
	    #i=i+1
