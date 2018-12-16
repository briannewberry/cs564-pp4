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
    t = transaction()
    try:
        db.update('CurrentTime', where = "1 == 1", Time = time)
    except Exception as e:
        t.rollback()
        print("Caught exception ", e.message)
        return False
    else:
        t.commit()
        return True


def getItemById(item_id):
    query_string = 'select * from Items where item_ID = $itemID'
    try:
        result = query(query_string, {'itemID': item_id})
    except Exception as e:
        return None
    return result[0]

def getSearchItems(item_ID, user_ID, category, minPrice, maxPrice, description, status):
    query_string = 'select DISTINCT i.ItemID, i.Seller_UserID, i.Currently, i.Buy_Price, i.Description, i.Started, i.Ends from Items i join Categories c on i.ItemID = c.ItemID'
    constraint = [];
    inputs = {};
    if (item_ID != ''):
        constraint.append('i.ItemID = $itemID')
        inputs['itemID'] = item_ID

    if (user_ID != ''):
        constraint.append('i.Seller_UserID = $userID')
        inputs['userID'] = user_ID

    if (category != ''):
        constraint.append('c.category = $category')
        inputs['category'] = category

    if (minPrice != ''):
        constraint.append('i.Currently >= $minPrice')
        inputs['minPrice'] = minPrice

    if (maxPrice != ''):
        constraint.append('i.Currently <= $maxPrice')
        inputs['maxPrice'] = maxPrice

    if (description != ''):
        description = '%' + description + '%'
        constraint.append('i.description like $description')
        inputs['description'] = description

    first = True
    for x in constraint:
        if first:
            query_string = query_string + ' where ' + x
            first = False
        else:
            query_string = query_string + " AND " + x

    t= transaction()
    try:
        result = query(query_string, inputs);
    except Exception as e:
        t.rollback()
        print str(e)
        return None
    else:
        t.commit()
        return result;

def addBid(itemID, userID, price):
    current_time = getTime()
    query_string = 'insert into Bids values ($ItemID, $UserID, $Price, $current_time)'

    t = transaction()
    try:
        result = db.query(query_string, {'ItemID': itemID, 'UserID': userID, 'Price': price, 'current_time': current_time})
    except Exception as e:
        t.rollback()
        print(e.message)
        return False
    else:
        t.commit() 
        return True

def getDetails(itemID):
    item = getItemById(itemID)
    # TODO 
    # get categories of item
    # get bids on item
    return item # catgory, bids


# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

def queryForTime(query_string, vars = {}):
    return db.query(query_string, vars)
#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
