from sqlalchemy import create_engine

from settings.database import SQL_ALCHEMY_DATABASE_URL

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)