from gettext import install
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")
@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars = mongo.db.mars.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars=mars)
# set our path to /scrape
@app.route("/scrape")
def scraper():
    # create a listings database
    mars = mongo.db.mars
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape_all()
    # update our listings with the data that is being scraped.
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)
if __name__ == "__main__":
    app.run(debug=True)












