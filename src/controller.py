from framework.controller.base import ControllerBase
from framework.controller.generator import generate_controller_response_dict

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

		data = ""

		username = self.request_dict['path_parameters']['username']

		if not username	== "":

			with engine.connect() as cnx:
				result = cnx.execute(
					"""
					SELECT * FROM users WHERE username="{}";
					""".format(username)
				)
				user = result.fetchone()
		
			if user is not None:

				data = {
					'id':user[0],
					'username':user[1],
					'handle':user[3],
					#'profile_image':user[4]
				}

				status_code = 200

			else:
				status_code = 404

				data = {
					"message": "Not Found"
				}

		else:
			with engine.connect() as cnx:
				result = cnx.execute(
					"""
					SELECT id, username
					FROM users;
					"""
				)
				users = result.fetchall()
			
			users_arr = []
			for user in users:
				user_dict = {
					'id':user[0],
					'username':user[1]
				}
				users_arr.append(user_dict)
	
			
			data = {
				'users':users_arr
			}
			status_code = 200


		data = json.dumps(data)
		controller_response_dict = generate_controller_response_dict(
			status_code=status_code,
			custom_headers={},
			body=data
		)

		return controller_response_dict