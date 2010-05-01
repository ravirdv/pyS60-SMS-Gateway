import inbox, e32, lightblue, threading, messaging

sndSkt = lightblue.socket()
sndSkt.connect(("11:11:11:11:11:11",1))
box=inbox.Inbox()


class SenderThread ( threading.Thread ):
   def __init__ ( self, no, response):
      self.no = no
      self.response = response
      threading.Thread.__init__ ( self )

   def run ( self ):
      print "Inside SEnder Thread :D"
      messaging.sms_send(self.no, response)
     


def callback(id):
    #id=box.sms_messages()[0]
    box=inbox.Inbox()
    sndSkt.send(box.content(id))
    response = sndSkt.recv(1024)
    print response
    SenderThread(box.address(id),response).start()
box.bind(callback)
print "Waiting for new SMS messages.."
app_lock = e32.Ao_lock()
app_lock.wait()
print "Sent To Pc"
sndSkt.close()
