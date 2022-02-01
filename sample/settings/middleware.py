from slowapi.middleware.security import AllowedHostMiddleware

MIDDLEWARES = [
	AllowedHostMiddleware,
]