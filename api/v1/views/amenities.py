#!/usr/bin/python3
"""amenities views"""
from models.amenity import Amenity
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
@app_views.route('/amenities', defaults={'amenity_id': None}, methods=['GET'])
def retrives_amenity(amenity_id):
    """Retrives the list of all amenitys"""
    if amenity_id is None:
        return jsonify([
            amenity.to_dict() for amenity in storage.all(Amenity).values()])

    if storage.get(Amenity, amenity_id) is None:
        abort(404)

    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity"""
    amenitys = storage.get(Amenity, amenity_id)
    if amenitys is None:
        abort(404)
    amenitys.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """creates a new amenity"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        abort(400, 'Missing name')
    amenity = Amenity(**json_data)
    amenity.save()
    # return a tuple default(data, status)
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update a amenity"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, values)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
