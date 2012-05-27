from sqlalchemy import Table, Column, ForeignKey, text
from sqlalchemy import Integer, Unicode, UnicodeText, DateTime

def mixin_cad(table):
    columns = [
        Column('created', DateTime, server_default=text('NOW()')),
        Column('created_by_id', Integer, ForeignKey('users.id')),
        Column('archived', DateTime),
        Column('archived_by_id', Integer, ForeignKey('users.id')),
        Column('deleted', DateTime),
        Column('deleted_by_id', Integer, ForeignKey('users.id'))
    ]
    for column in columns:
        table.append_column(column)

def mixin_tags_json(table):
    Column('tags', Unicode),
    Column('json', UnicodeText),

def load(meta, engine, *tables):
    for table in tables:
        Table(table, meta, autoload=True, autoload_with=engine)
