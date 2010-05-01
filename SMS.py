# -*- coding: utf-8 -*-
import sys
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

#def main():
#  s = SMS()
#  print s
#  print s.to

#if __name__=="__main__":
#  main()