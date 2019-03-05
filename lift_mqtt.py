import paho.mqtt.client as mqtt
import time



class Lift_MQTT:

    connected = False

    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("umrrkhdc","fQyYcpqZUXo5")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self,button_callback):
        self.button_callback = button_callback

        try:
            self.client.connect_async("m15.cloudmqtt.com", 11684, 60)
            self.client.loop_start()
            pass
        except:
            return False
            

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.connected = True

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("boatlift/command")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print('MQTT')
        print('MQTT Message: Topic {}, Payload {}'.format(msg.topic,msg.payload.decode("utf-8")))
  
        self.button_callback(msg.payload.decode("utf-8"),'')


    def publish(self,msg,payload):
        self.client.publish ("boatlift/"+msg,payload)

def dummy (mode):
    print (mode)
    if mode is "STOP":
        print ("stop")



if __name__ == '__main__':
    try:
        client = Lift_MQTT()
        client.connect(dummy)
        while True:
            time.sleep(.5)
            #client.publish("boat","lift")

    except KeyboardInterrupt:
        print("Measurement stopped by User")
