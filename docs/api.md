# Basement Closet API

The Basement Closet service will assist us in keeping track of the loose computer parts we have around the house.

In order to keep track of these parts, we need a system that will allow us to save info about a part, it's general location, purpose, etc.

This API will generally follow the CRUD model:
- Create
- Read
- Update
- Delete

For this project, we would like to have the following operations:

- Create an inventory and retrieval process (the data store)
- Input values and strings into the data store
- Access and output sets of values and strings from data store
- Access and alter individual comments and strings from data store
- Delete items from the data store
- Comment and note tracking for each individual part/item from data store
- Return items from data store by part type

## REST API

- `PUT /inventory` - Create/Update an item in the inventory
- `GET /inventory` - Retrieve an item from the inventory with filtering based on query params
- `DELETE /inventory/{item-id}` - Delete an item by ID
- `POST /inventory/comment/{item-id}` - Post a new comment to an item
- `DELETE /inventory/comment/{comment-id}` - Delete a comment