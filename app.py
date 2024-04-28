from flask import Flask,request,jsonify

from datetime import datetime, timezone

from dotenv import load_dotenv

import os

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app = Flask(__name__)

cors = CORS()

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_DATABASE_USER')}:{os.getenv('MYSQL_DATABASE_PASSWORD')}@host.docker.internal/{os.getenv('MYSQL_DATABASE_NAME')}"

cors.init_app(app)

db= SQLAlchemy(app)


class Places(db.Model):
    id=db.Column(db.Integer, primary_key=True )
    lat=db.Column(db.String(100), nullable=False)
    lng=db.Column(db.String(100), nullable=False)
    created_date=db.Column(db.DateTime,default=datetime.now(timezone.utc).astimezone())

with app.app_context():
    db.create_all()
print(datetime.now(timezone.utc).astimezone())
@app.route("/get-places")
def get_places():
    try:
        datas = db.session.query(Places).all()
        return [
        {
            "id": data.id,
            "lat": data.lat,
            "lng": data.lng,
            "created_date": data.created_date
        } for data in datas
        ]
    except Exception as error:
        return jsonify({'error': error})
@app.route("/add-place", methods = [ 'POST'])
def add_place():
    rdata = request.get_json()

    new_place = Places(
        lat= rdata["lat"],
        lng= rdata["lng"],
        )
    try:
        db.session.add(new_place)
        db.session.commit()
        datas = db.session.query(Places).all()
        return [
        {
            "id": data.id,
            "lat": data.lat,
            "lng": data.lng,
            "created_date": data.created_date
        } for data in datas
        ]
    except Exception as error:
        return jsonify({'error': error})
    
@app.route("/delete-place/<place_id>",methods=["DELETE"])
def delete_place(place_id):
    delete_place = db.session.query(Places).where(Places.id == place_id).first()
    try:
        db.session.delete(delete_place)
        db.session.commit()

        datas = db.session.query(Places).all()
        return [
        {
            "id": data.id,
            "lat": data.lat,
            "lng": data.lng,
            "created_date": data.created_date
        } for data in datas
        ]
    except Exception as error:
        return jsonify({'error': error})
    
if __name__ == '__main__':
       app.run()