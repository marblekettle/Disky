from atproto import Client
from time import sleep

# BskyListener logs into an account with a username and valid app password
# and in regular intervals fetches the latest post by that account. The
# "run" method needs to run parallel on a separate thread to not be
# blocking.

class BskyListener:
	def __init__(self, interval=60):
		self.client = Client()
		self.running = False
		self.queue = []
		self.interval = interval

	def	run(self, username, password):
		self.running = True
		profile = self.client.login(username, password)
		posturi = self.getLatestPost(profile.did).post.uri
		while self.running:
			sleep(self.interval)
			feed = self.getLatestPost(profile.did)
			if feed.post.uri != posturi:
				posturi = feed.post.uri
				self.queue.append(feed.post)

	def	getLatestPost(self, did):
		return self.client.get_author_feed(actor=did,
			filter='posts_no_replies', limit=1).feed[0]

	def pollQueue(self):
		if len(self.queue) == 0:
			return None
		out = self.queue[0]
		self.queue = self.queue[1:]
		return out

	def stop(self):
		self.running = False