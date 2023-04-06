from flask import Flask, render_template, redirect, request, abort
from .web_utils import *
import math
import json
# connect database


app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/category/laptop")

@app.route("/category/<table_name>")
def category(table_name):
    table_name = table_name.replace("-", "_")
    return render_template("category_page.html", 
                           categories=get_category(), 
                           parameters=get_parameters(table_name), 
                           product_info=filter_product(table_name))

@app.route("/filterProduct", methods=["POST"])
def filterProduct():
    table_name = request.args.get("c")
    if table_name == None:
        abort(404)
    table_name = str(table_name).replace("-", "_")

    page_index = to_int(request.args.get("pi"), 0)    
    product_per_page = to_int(request.args.get("size"), 20)
    sort_type = to_int(request.args.get("sort-type"), 0)
    filters = request.json
    return json.dumps(filter_product(
        table_name=table_name,
        page_index=page_index,
        product_per_page=product_per_page,
        sort_type=sort_type,
        filters=filters
    ))