#test mode
from app import app
#server mode
#from FlaskApp.app import app
# dude these schema things should not be in the view.. this basically means
# everytime when you refresh the page you have to reconnect the server??
# I believe this should be in init file and the you shoudl find a way to maintain through model.
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, request
from app.schema.tweets import Tweets_sche
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from logging import Formatter, FileHandler

#Setup the logger
LOGGER = logging.getLogger('streamer_logger')
file_handler = FileHandler('streamer.log')
handler = logging.StreamHandler()
file_handler.setFormatter(Formatter(
        '%(thread)d %(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))
handler.setFormatter(Formatter(
        '%(thread)d %(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))
LOGGER.addHandler(file_handler)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/barchart")
def bar():
    #----DB INIT BEGIN---------------------------------------------

    MONGO_HOST = '162.243.122.37'
    MONGO_PORT = 27017

    #Try to connect to MongoDB
    try:
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client.tinyjumbo
        tweet_collection = db.tcount
        LOGGER.info('connecting to DB...')
        print "Successfully connect to DB ---"

    except ConnectionFailure:
        LOGGER.error('Could not connect to MongoDB, aborting Flask app...')
        sys.exit(-1)
	#----DB INIT END---------------------------------------------


    #read from DB and store it
    print "start to get collections"
    data_set = []
    date_set = []
    count_set = []
    print "create an empty set"
    now = datetime.now()
    start = datetime(2016, 2, 18, 20, 01, 01)
    end = datetime(2016, 2, 19,20 , 01, 04)
    db_read = tweet_collection.find({'date': {'$gte': start, '$lt': end}}).sort([("company",pymongo.ASCENDING)])
    db_read_num = tweet_collection.find({'date': {'$gte': start, '$lt': end}}).count()
    #db_read = tweet_collection.find_one()
    print db_read
    print db_read_num
    print "succeed to read"
    LOGGER.info('Reading data from db...')
    for i in db_read:
        count_set.append(i["count"])
    '''
    for data in db_read:
        print "start to reformat data"
        d = Tweets_counter(data["company"],data["count"],data["date"])
        data_set.append(d)
    '''
    return render_template('barchart.html',info=count_set)




















