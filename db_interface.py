"""
db_interface

A package for getting content off reddit, and sometimes putting it there

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR, Jason
@licence    GNU GPL v.3
"""
import os
from peewee import *

DIR = os.path.dirname(os.path.realpath(__file__))
database = SqliteDatabase("{}/already_done.sqlite".format( DIR ), **{})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class AlreadyDone(BaseModel):
    id = PrimaryKeyField(db_column='ID')
    subID = CharField(db_column='subid')

    class Meta:
        db_table = 'already_done'

def getSub(subID):
    for i in AlreadyDone.select(AlreadyDone.subID).where(AlreadyDone.subID == subID):
        return i
    return None

def getMostRecent():
    for i in AlreadyDone.select(AlreadyDone.subID).order_by(AlreadyDone.id.desc()):
        return i.subID
    return None

def addSub(subID):
    return AlreadyDone.create(subID = subID)

AlreadyDone.create_table(True)
