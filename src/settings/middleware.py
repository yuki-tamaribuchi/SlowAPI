from framework.middleware.security import AllowedHostMiddleware

MIDDLEWARES = [
	AllowedHostMiddleware,
]