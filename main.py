# -*- coding: utf-8 -*-
from db import database
from parser import SMSParser
import time
from GTalk import GTalk
from Facebook import Facebook
db=database()
gt={}
fb={}
loggedin={}
def Glogin(mobno,user,password):
  if mobno in loggedin and loggedin[mobno]:
    gt[mobno]=GTalk(mobno)
    if not gt[mobno].connect(user, password):
      db.pushOutboxMsg(mobno, "Invalid GTalk user or password! Access Denied!")
    else:
      gt[mobno].start()
      time.sleep(5)
      users=gt[mobno].getOnlineUsers()
      response=""
      for item in users:
	response+="G%s/%s\f\r" % (item, users[item])
      db.pushOutboxMsg(mobno, response)
  else:
    db.pushOutboxMsg(mobno, "Please login... Reply with LOGIN password to login.")

def Flogin(mobno,user,password):
  if mobno in loggedin and loggedin[mobno]:
    fb[mobno]=Facebook(mobno)
    if not fb[mobno].connect(user, password):
      db.pushOutboxMsg(mobno, "Invalid facebook user or password! Access Denied!")
    else:
      fb[mobno].start()
      time.sleep(5)
      users=fb[mobno].getOnlineUsers()
      response=""
      for item in users:
	response+="F%s/%s\n" % (item, users[item])
      db.pushOutboxMsg(mobno, response)
  else:
    db.pushOutboxMsg(mobno, "Please login... Reply with LOGIN password to login.")

while 1:
  time.sleep(3)
  rows = db.popInboxMsg()
  for row in rows:
    db.setInboxProcessed(row[0], 1)
    print "Msg : -> %s %s %s %s %s %s" % (row[0], row[1], row[2], row[3], row[4], row[5])
    r=SMSParser.parseSMS(row[3])
    if not r[0]:
      db.pushOutboxMsg(row[2], "Invalid keyword!")
    else:
      if r[1]=="register":
	if not db.isUserExists(row[2]):
	  db.pushNewUser(row[2],r[2])
	  db.pushOutboxMsg(row[2], "Registered! Send LOGIN password as reply to login.")
	else:
	  db.pushOutboxMsg(row[2], "User already exists!")
      elif r[1]=="pw":
	if row[2] in loggedin and loggedin[row[2]]:
	  if db.setNewPassword(row[2],r[2]):
	    db.pushOutboxMsg(row[2], "Password Changed!")
	else:
	  db.pushOutboxMsg(row[2], "Please login... Reply with LOGIN password to login.")
      elif r[1]=="login":
	if db.isUserCorrect(row[2],r[2]):
	  response="Login success! "
	  loggedin[row[2]]=True
	  gl=db.getAccount(row[2],"google")
	  if gl!=None:
	    Glogin(row[2],gl[0],gl[1])
	    response+="Logging you in GTALK... "
	  fl=db.getAccount(row[2],"facebook")
	  if fl!=None:
	    Flogin(row[2],fl[0],fl[1])
	    response+="Logging you in facebook... "
	  db.pushOutboxMsg(row[2], response)
	else:
	  db.pushOutboxMsg(row[2], "Invalid Password or not a registered!")
      elif r[1]=="logout":
	if row[2] in gt:
	  gt[row[2]].disconnect()
	  del gt[row[2]]
	if row[2] in fb:
	  fb[row[2]].disconnect()
	  del fb[row[2]]
	if row[2] in loggedin:
	  loggedin[row[2]]=False
	  del loggedin[row[2]]
      elif r[1]=="glogin":
	Glogin(row[2],r[2],r[3])
	db.pushNewService(row[2],"google",r[2], r[3])
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
	Flogin(row[2],r[2],r[3])
	db.pushNewService(row[2],"facebook",r[2], r[3])
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