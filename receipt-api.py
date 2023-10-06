from flask import Flask, request
import uuid
import re
import math
import json

app = Flask(__name__)


database = {}


@app.post("/receipts/process")
def process_receipts(receipt=None):

    if receipt is None: # This is added so that we can pass a recipt to this function for the testing below
        receipt = request.get_json(force=True, silent=True)
        if receipt is None:
            return "Please add a JSON body with a receipt."

    unique_identifier = uuid.uuid4()

    database[unique_identifier] = receipt

    return {"id": unique_identifier}


@app.get("/receipts/<uuid:id>/points")
def get_receipt_points(id):
    try:
        receipt = database[id]
    except KeyError:
        return "Receipt with that UUID does not exist. Try again with a valid UUID."

    points = calculate_receipt_points(receipt=receipt)

    return {"points": points}


@app.get("/receipts/<any_non_uuid>/points")
# I wanted to try using the Variable Rules Converter types above,
# this is here to catch someone trying to go to "/receipts/<uuid:id>/points" but not using a valid UUID
def return_error_if_not_valid_uuid(any_non_uuid):
    return f"{any_non_uuid} is not a valid UUID. Please try again with a valid UUID."


def calculate_receipt_points(receipt):
    points = 0

    points += len(re.sub(r'\W+', '', receipt["retailer"]))

    if not (float(receipt["total"]) % 1.00):
        points += 75 # This can be 75 instead of 50 because if it is divisible by 1.00 it will always
                     # be divisible by 0.25 and that lets us use an elif below saving one calculation.
                     # I'd argue its better here to not do it this way and always calculate twice just
                     # to make it more readable but I wanted to show a bit of out-of-the-box thinking!
    elif not (float(receipt["total"]) % 0.25):
        points += 25

    points += int(len(receipt["items"]) / 2) * 5

    for item in receipt["items"]:
        if not (len(item["shortDescription"].strip()) % 3):
            points += math.ceil(float(item["price"]) * 0.2)

    if (int(receipt["purchaseDate"][-1]) % 2):
        points += 6

    purchase_time = float(receipt["purchaseTime"].replace(":", ".")) # Turns the time format into a float!
    if (purchase_time > 14 and
        purchase_time < 16):
        points += 10

    return points


# ||||||||||||||||||||||||||||||||||||||||||
print("-------- Tests --------") # This will show the results of both endpoints in the console using the /example receipts
print()
print("morning-receipt:")
morning_receipt_json_file = open("./examples/morning-receipt.json")
morning_receipt = json.load(morning_receipt_json_file)
morning_receipt_results = process_receipts(morning_receipt)
print("/receipts/process results:", morning_receipt_results)
print("/receipts/<uuid:id>/points results:", get_receipt_points(morning_receipt_results["id"]))
print()
print("simple-receipt:")
simple_receipt_json_file = open("./examples/simple-receipt.json")
simple_receipt = json.load(simple_receipt_json_file)
simple_receipt_results = process_receipts(simple_receipt)
print("/receipts/process results:", simple_receipt_results)
print("/receipts/<uuid:id>/points results:", get_receipt_points(simple_receipt_results["id"]))
print()
print("-----------------------")
print()
# ||||||||||||||||||||||||||||||||||||||||||


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
