from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required and can't left empty"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must have a store id."
                        )
###########################################################################
# This method was used when we used in-memory items list
###########################################################################
#     @jwt_required()
#     def get(self, name):
#         # next() function on top of filter
#         item = next(filter(lambda x: x['name'] == name, items), None)
# #        for item in items:
# #            if item['name'] == name:
# #                return item
#         return {'item': item}, 200 if item else 404

###########################################################################
# This part uses database for items
###########################################################################
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found!'}, 404


##################################################################################################
# This method was used when we used in-memory items list
##################################################################################################
    # def post(self, name):
    #     if next(filter(lambda x: x['name'] == name, items), None) is not None:
    #         return {'message': "An item with name '{}' already exists.".format(name)}, 400
    #
    #     # we could pass 'force = True' or 'silent=True' in get_json() to ignore the mismatch/error in provided data
    #     request_data = Item.parser.parse_args()
    #     new_item = {'name': name, 'price': request_data['price']}
    #     items.append(new_item)
    #     return new_item, 201

###########################################################################
# This part uses database for items
###########################################################################
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            # Bad request
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        request_data = Item.parser.parse_args()
        new_item = ItemModel(name, request_data['price'], request_data['store_id'])

        try:
            new_item.save_to_db()
        except:
            # Internal server error
            return {"message": "An error occurred inserting the item"}, 500

        return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted!'}

    ##################################################################################################
    # This method was used when we used in-memory items list
    ##################################################################################################
    # def put(self, name):
    #     data = Item.parser.parse_args()
    #
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item is None:
    #         item = {'name': name, 'price': data['price']}
    #         items.append(item)
    #     else:
    #         item.update(data)
    #     return item

###########################################################################
# This part uses database for items
###########################################################################
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # results = cursor.execute(query)
        #
        # items = []
        # for row in results:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()

        return {"item": [item.json() for item in ItemModel.query.all()]}
        # Another way of implementing using lambda function as follows
        # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}
