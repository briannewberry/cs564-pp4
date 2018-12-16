import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    #
    query_string = 'select Time from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].Time # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!

def updateTime(time):
    db.update('CurrentTime', where = "1 == 1", Time = time)
    return

def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where item_ID = $itemID'
    result = query(query_string, {'itemID': item_id})
    return result[0]

def getSearchItems(item_ID, user_ID, minPrice, maxPrice, status):
    query_string = 'select * from Items'
    constraint = [];
    inputs = {};
    if (item_ID != ''):
        constraint.append('ItemID = $itemID')
        inputs['itemID'] = item_ID

    if (user_ID != ''):
        constraint.append('Seller_UserID = $userID')
        inputs['userID'] = user_ID

    if (minPrice != ''):
        constraint.append('Currently >= $minPrice')
        inputs['minPrice'] = minPrice

    if (maxPrice != ''):
        constraint.append('Currently <= $maxPrice')
        inputs['maxPrice'] = maxPrice

    first = True
    for x in constraint:
        if first:
            query_string =query_string + ' where ' + x
            first = False
        else:
            query_string = query_string + " AND " + x

    result = query(query_string, inputs);
    return result;

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

def queryForTime(query_string, vars = {}):
    return db.query(query_string, vars)
#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
