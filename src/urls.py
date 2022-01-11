from controller import sample_controller, SampleController, UsersController

url_patterns = [
	{'url':'sample' ,'controller':SampleController},
	{'url':'users/<username>/', 'controller':UsersController},
	{'url':'users/<username>/entry/<entry_id>', 'controller':None}
]