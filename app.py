from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_DB"
mongo = PyMongo(app)


@app.route("/")
def index():
    Mars_scrape = mongo.db.Mars_scrape.find_one()
    return render_template("index.html", Mars_scrape=Mars_scrape)

@app.route("/scrape")
def scraper():

    Mars_scrape = mongo.db.Mars_scrape
    scrape_data = scrape_mars.scrape()
    Mars_scrape.update({}, scrape_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
