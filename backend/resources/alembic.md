## Create alembic directory
`alembic init -t async alembic` 

## Folder/File Descriptions
- versions -> where migration files will go
- env.py -> config
- script.py.mako -> template for generating new migrations
- alembic.ini (in root)

## Update
1. Update `alembic.ini`: sqlalchemy.url
2. Update `alembic/env.py` 

## Migrations
`alembic revision --autogenerate -m "some message"` -> creates migration file, does not apply anything to database
`alembic upgrade head` -> apply all migrations up to latest versions
`alembic current` -> show which migration you are on