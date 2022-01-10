from framework.controller.base import ControllerBase

from database import engine

def sample_controller(request_dict):
	def get(request_dict):
		return 'Hello from sample controller'

class SampleController(ControllerBase):

	def get(self):
		return 200, {}, 'Hello from SampleController Get'
	
	def post(self):
		return 200, {}, 'Hello from SampleController Post. We got {}'.format(self.request_dict['body'])

	def put(self):
		return 200, {}, 'Hello from SampleController Put. We got {}'.format(self.request_dict['body'])

	def delete(self):
		return 200, {}, 'Hello from SampleController Delete.'


class UsersController(ControllerBase):

	def get(self):
		import json


		with engine.connect() as cnx:
			result = cnx.execute(
				"""
				SELECT * FROM users WHERE username="yuki";
				"""
			)
			user = result.fetchone()

		data = {
			'id':user[0],
			'username':user[1],
			'handle':user[3],
			#'profile_image':user[4]
		}

		data = json.dumps(data)

		return 200, {}, data