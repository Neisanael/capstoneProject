import json
from flask import Flask, jsonify, request
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.model import Recipe, UserRecipeRating
import model.filter as filter

app = Flask(__name__)

engine_str = (
      "mysql+pymysql://{user}:{password}@{server}/{database}".format(
       user      =  "root",
       password  =  "qwerty12345",
       server    =  "34.101.54.86",
       database  =  "capstone"))
engine = sa.create_engine(engine_str)
Session = sessionmaker(bind=engine)

with open("clean_recipes.json") as f:
    recipes = json.load(f)


@app.route('/', methods=['GET'])
def test():
    return 'Put URL'


@app.route('/api/rating/<int:recipe_id>', methods=['GET'])
def get_rating(recipe_id):
    try:
        session = Session()
        result = session.execute(select(UserRecipeRating).where(UserRecipeRating.recipe_id == recipe_id))
        ratings = [dict(row) for row in result]
        average_rating = round(sum(ratings) / len(ratings), 2) if ratings else None
        session.close()
        return jsonify({
            'ratings': ratings,
            'average_rating': average_rating
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to fetch ratings'}), 500


@app.route('/api/rating', methods = ['POST'])
def post_rating():
    try:
        session = Session()
        data = request.get_json()
        new_rating = UserRecipeRating(
            user_id=data['user_id'],
            recipe_id=data['recipe_id'],
            date=data['date'],
            rating=data['rating']
        )
        session.add(new_rating)
        session.commit()
        session.close()
        return jsonify({'message': 'Rating added successfully'}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to add rating'}), 500


@app.route('/api/rating', methods = ['PUT'])
def put_rating():
    try:
        session = Session()
        data = request.get_json()
        existing_rating = session.query(UserRecipeRating).filter_by(
            user_id=data['user_id'],
            recipe_id=data['recipe_id']
        ).first()
        if existing_rating:
            existing_rating.rating = data['new_rating']
            session.commit()
            session.close()
            return jsonify({'message': 'Rating updated successfully'}), 200
        else:
            session.close()
            return jsonify({'error': 'Rating not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to update rating'}), 500


@app.route('/api/rating', methods = ['DELETE'])
def delete_rating():
    try:
        session = Session()
        data = request.get_json()
        rating_to_delete = session.query(UserRecipeRating).filter_by(
            user_id=data['user_id'],
            recipe_id=data['recipe_id']
        ).first()
        if rating_to_delete:
            session.delete(rating_to_delete)
            session.commit()
            session.close()
            return jsonify({'message': 'Rating deleted successfully'}), 200
        else:
            session.close()
            return jsonify({'error': 'Rating not found'}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to delete rating'}), 500


@app.route("/recipes", methods=["GET"])
def get_recipes():
    return jsonify(recipes)

@app.route("/predict", methods=["POST"])
def get_predict():
    data = request.get_json(force=True)
    filtered = filter.predict(list(data["ingres"]), recipes)
    prediction = filter.ranking(data["user_id"], filtered)
    extracted_values = [int(item[0]) for item in prediction]
    results_from_database = search_database_by_ids(extracted_values)
    return jsonify(results_from_database)

def search_database_by_ids(ids):
    try:
        session = Session()
        results = session.query(Recipe).filter(Recipe.id.in_(ids)).all()
        session.close()
        return [result.__dict__ for result in results]
    except Exception as e:
        print("Error:", e)
        return {'error': 'Failed to fetch data from the database'}, 500

if __name__ == '__main__':
    app.run(debug=True)
