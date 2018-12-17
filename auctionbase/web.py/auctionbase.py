#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the
reload(sys)
sys.setdefaultencoding('utf8')
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

 # @group Brian Newberry, Travis Johnson, Teryl Schmidt
 # @id 9073555451, 9072937378, 9072604920

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
#current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        '/search', 'search',
        '/add_bid', 'add_bid',
        '/', 'home',
        '/item_detail', 'item_detail'
        # TODO: add additional URLs here
        # first parameter => URL, second parameter => class name
        )

class home:
    # A simple GET request, to '/'
    def GET(self):
        return render_template('app_base.html')

class curr_time:
    # A simple GET request, to '/currtime'
    #
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']


        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        if sqlitedb.updateTime(selected_time) == False:
            return render_template('select_time.html', message = "Could not update time")
        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)


class search:
    def GET(self):
        return render_template('search.html', search_result = False)

    def POST(self):
        post_params = web.input()
        itemID = post_params['itemID']
        userID = post_params['userID']
        Category = post_params['Category']
        minPrice = post_params['minPrice']
        maxPrice = post_params['maxPrice']
        Description = post_params['Description']
        status = post_params['status']

        if itemID or userID or Category or minPrice or maxPrice or Description:
            update_message = 'Complete'
            result = sqlitedb.getSearchItems(itemID, userID, Category, minPrice, maxPrice, Description, status);
            timeNow = string_to_time(sqlitedb.getTime())

            if (status == 'open'):
                for x in result:
                    if (string_to_time(x['Started']) >= timeNow and string_to_time(x['Ends']) < timeNow):
                        filtered.append(x);
            elif (status == 'close'):
                for x in result:
                    if (string_to_time(x['Ends']) < timeNow):
                        filtered.append(x);
            elif (status == 'notStarted'):
                for x in result:
                    if (string_to_time(x['Started']) > timeNow):
                        filtered.append(x);
            else:
                filtered = result;       
        else:
            filtered = []
            update_message = 'No inputs'

        return render_template('search.html', message = update_message, search_result = filtered)

class add_bid:
    # A simple GET request, to '/add_bid'
    def GET(self):
        return render_template('add_bid.html')

    def POST(self):
        post_params = web.input()
        itemID = post_params['itemID']
        userID = post_params['userID']
        price = post_params['price']

        result = sqlitedb.addBid(itemID, userID, price)

        return render_template('add_bid.html', add_result = result)

class item_detail:
    def GET(self):
        itemID = web.input().id
        itemInfo = sqlitedb.getItemById(itemID)
        categories = sqlitedb.getItemCategories(itemID)
        bids = sqlitedb.getItemBids(itemID)
        winner = sqlitedb.getWinner(itemID)

        return render_template('item_detail.html', itemID = itemID, itemInfo = itemInfo, Categories = categories, Bids = bids, Winner = winner) 

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
