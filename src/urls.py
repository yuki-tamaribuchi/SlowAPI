from controller import sample_controller, SampleController, UsersController

from framework.middleware.security import AllowedHostMiddleware, SQLInjectionProtectMiddleware
from framework.middleware.sample import PrintRequestMiddleware, PrintResponseMiddleware

#{'url':'任意のURL', 'controller':任意のControllクラス, 'middlewares':[任意のミドルウェアクラス<0個以上>]}
#パスパラメータは<>で括る
#{'url':, 'controller':, 'middlewares':[]} <-コピペ用

url_patterns = [
	{'url':'sample' ,'controller':SampleController, 'middlewares':[]},
	{'url':'users/<username>', 'controller':UsersController, 'middlewares':[SQLInjectionProtectMiddleware, PrintRequestMiddleware, PrintResponseMiddleware]},
	{'url':'users/<username>/entry/<entry_id>', 'controller':None, 'middlewares':[]},
	{'url':'sample/sample/<username>', 'controller':SampleController, 'middlewares':[]}
]