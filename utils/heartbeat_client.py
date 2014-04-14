import socket, time


class HeartBeatClient:

	def __init__(self):
		self.SERVER_IP = '127.0.0.1'
		self.SERVER_PORT = 43278
		self.BEAT_PERIOD = 5
		self.hb_msg = 'PyHB'

	def run_heartbeat_client(self):
		print ('Sending heartbeat to IP %s , port %d\n press Ctrl-C to stop\n') % (self.SERVER_IP, self.SERVER_PORT)
		while True:
			hbSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			hbSocket.sendto(self.hb_msg, (self.SERVER_IP, self.SERVER_PORT))
			time.sleep(self.BEAT_PERIOD)

if __name__ == '__main__':
	hb_client = HeartBeatClient()
	hb_client.run_heartbeat_client()
