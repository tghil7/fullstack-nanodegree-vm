from flask import Flask, render_template, url_for, request ,flash, redirect, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, HouseItem, FurnitureItem, CarItem

engine = create_engine('postgresql:///catalogmenu')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories')
def goodCategories():
    categories = session.query(Category).distinct(Category.name).group_by(Category.name, Category.id)
    latestCars = session.query(CarItem).order_by((CarItem.id).desc()).limit(2)
    latestHouses = session.query(HouseItem).order_by((HouseItem.id).desc()).limit(2)
    latestFurnitures = session.query(FurnitureItem).order_by((FurnitureItem.id).desc()).limit(2)
    return render_template("home.html", categories = categories, latestCars = latestCars, latestHouses = latestHouses, latestFurnitures = latestFurnitures)




@app.route('/categories/<int:category_id>/menu')
def goodCategoryItems(category_id):
    category = session.query(Category).filter_by(id= category_id).one()
    if category.name == "Cars":
        items = session.query(CarItem).all()
    elif category.name == "House":
        items = session.query(HouseItem).all()
    elif category.name == "Furniture":
        items = session.query(FurnitureItem).all()
    return render_template('categories.html', category_id = category_id, items = items, category = category)

@app.route('/categories/cars')
def carCategory():
    return "All cars in the category will show up here"

@app.route('/categories/cars/<int:car_id>/options')
def carOptions(car_id):
    return "The car options are the following for " + str(car_id)






if __name__== '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    
