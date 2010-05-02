# -*- coding: utf-8 -*-
from db import database
from parser import SMSParser
import time
from GTalk import GTalk
from Facebook import Facebook
db=database()
gt={}
fb={}
while 1:
  time.sleep(3)
  rows = db.popInboxMsg()
  for row in rows:
    db.setInboxProcessed(row[0], 1)
    print "Msg : -> %s %s %s %s %s %s" % (row[0], row[1], row[2], row[3], row[4], row[5])
    r=SMSParser.parseSMS(row[3])
    if not r[0]:
      db.pushOutboxMsg(row[2], "Invalid keyword")
    else:
      if r[1]=="register":
	if not db.isUserExists(row[2],r[2]):
	  db.pushNewUser(row[2],r[2])
	else:
	  db.pushOutboxMsg(row[2], "User already exists!")
      elif r[1]=="login":
	pass
      elif r[1]=="glogin":
	gt[row[2]]=GTalk(row[2])
	if not gt[row[2]].connect(r[2], r[3]):
	  db.pushOutboxMsg(row[2], "Invalid GTalk user or password! Access Denied!")
	else:
	  gt[row[2]].start()
	  time.sleep(5)
	  users=gt[row[2]].getOnlineUsers()
	  response=""
	  for item in users:
	    response+="G%s/%s\n" % (item, users[item])
	  db.pushOutboxMsg(row[2], response)
      elif r[1]=="glist":
	if row[2] in gt:
	  users=gt[row[2]].getOnlineUsers()
	  response=""
	  for item in users:
	    response+="G%s/%s\n" % (item, users[item])
	  db.pushOutboxMsg(row[2], response)
	else:
	   db.pushOutboxMsg(row[2], "Please login first...")
      elif r[1]=="glogout":
	if row[2] in gt:
	  gt[row[2]].disconnect()
	  del gt[row[2]]
      elif r[1]=="gim":
	if row[2] in gt:
	  if not gt[row[2]].sendImFromId(r[2],r[3]):
	    db.pushOutboxMsg(row[2], "Invalid GID")
	else:
	   db.pushOutboxMsg(row[2], "Please login first...")
      elif r[1]=="flogin":
	fb[row[2]]=Facebook(row[2])
	if not fb[row[2]].connect(r[2], r[3]):
	  db.pushOutboxMsg(row[2], "Invalid FB user or password! Access Denied!")
	else:
	  fb[row[2]].start()
	  time.sleep(5)
	  users=fb[row[2]].getOnlineUsers()
	  response=""
	  for item in users:
	    response+="F%s/%s\n" % (item, users[item])
	  db.pushOutboxMsg(row[2], response)
      elif r[1]=="flist":
	if row[2] in fb:
	  users=fb[row[2]].getOnlineUsers()
	  response=""
	  for item in users:
	    response+="F%s/%s\n" % (item, users[item])
	  db.pushOutboxMsg(row[2], response)
	else:
	   db.pushOutboxMsg(row[2], "Please login first...")
      elif r[1]=="flogout":
	if row[2] in fb:
	  fb[row[2]].disconnect()
	  del fb[row[2]]
      elif r[1]=="fim":
	if row[2] in fb:
	  if not fb[row[2]].sendImFromId(r[2],r[3]):
	    db.pushOutboxMsg(row[2], "Invalid FID")
	else:
	   db.pushOutboxMsg(row[2], "Please login first...")
      else:
	print "you missed a condition"
    #res = "1"
    #delete
    #res = conn2.recv(1024)
    #print res
    #while (res != "1" and res != "2"):
      #res = conn2.recv(1024)
      #print res
    #db.setProcessed(str(row[0]), res) 
#gt=GTalk("9898098980")
#if not gt.connect("vishal.dhawani", "Dhawani001"):
  #print "Response: Invalid user or password"
#else:
  #gt.start()
  #time.sleep(5)
#  gt.getOnlineUsers()
r=SMSParser.parseSMS("g123 hi")
for i in r:
  print i