# -*- coding: utf-8 -*-
class SMSParser:
  @staticmethod
  def parseSMS(msg):
    r=[False,False,False,False]
    #r.append(True)
    msg=msg.strip()
    s=msg.split(" ",1)
    if len(s)==1:
      if s[0].lower()=="glist" or s[0].lower()=="glogout" or s[0].lower()=="flist" or s[0].lower()=="flogout" or s[0].lower()=="logout":
	r[1]=s[0].lower()
	r[0]=True
    elif len(s)!=2:
      r[0]=False
    else:
      if s[0].lower()=="register" or s[0].lower()=="login" or s[0].lower()=="pw":
	r[0]=True
	r[1]=s[0].lower()
	r[2]=s[1]
      elif s[0].lower()=="glogin" or s[0].lower()=="flogin":
	r[1]=s[0].lower()
	y=s[1].split(" ",1)
	if len(y)!=2:
	  r[0]=False
	else:
	  r[0]=True
	  r[2]=y[0].replace("@gmail.com", "")
	  r[3]=y[1]
      elif s[0][0].lower()=="g":
	r[1]="gim"
	r[0]=True
	r[2]=""
	for i in range(1,len(s[0])):
	  r[2]+=s[0][i]
	r[3]=s[1]
      elif s[0][0].lower()=="f":
	r[1]="fim"
	r[0]=True
	r[2]=""
	for i in range(1,len(s[0])):
	  r[2]+=s[0][i]
	r[3]=s[1]
    return r



#REGISTER USERID PASSWORD
#LOGIN USERID PASSWORD
#GTALK USERID PASSWORD
#YAHOO USERID PASSWORD
#FACEBOOK USER PASSWORD
#
#GLIST
#YLIST
#
#G123 MSG

#R[0]=TRUE/FALSE
#R[1]=REGISTRATION/LOGIN/IM/GLOGIN/YLOGIN/FLOGIN/GLIST/YLIST/FLIST
#R[2]=USERNAME/ID/EMPTY
#R[3]=PASSWORD/msg/EMPTY