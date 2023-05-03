import mysql.connector
from flask import render_template
import regex as re

def count_product(table_name):
    if not table_name:
        return None
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="crawl_database"
    )
    cursor = db.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    amount = cursor.fetchall()
    return amount[0][0]

def get_category():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="crawl_database"
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    categories = []
    for row in cursor.fetchall():
        if row[0] == "Other":
            continue
        categories.append((str(row[0]).replace("_", " ")))
    
    categories.append("Other")
    return categories

def get_parameters(table_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="crawl_database"
    )
    cursor = db.cursor()
    cursor.execute(f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'crawl_database'""")
    parameter_names = cursor.fetchall()

    parameters = []
    for row in parameter_names:
        parameter_name = str(row[0])
        if parameter_name.lower() in ["cpu", "chip", "name", "url", "price", "id", "image_path"]:
            continue

        parameter = {
            "name": str(parameter_name).replace("_", " "),
            "values": set()
        }

        cursor.execute(f"""
        SELECT DISTINCT {parameter_name}
        FROM {table_name}
        WHERE {parameter_name} IS NOT NULL
        """)
        data = cursor.fetchall()

        for row in data:
            for value in str(row[0]).split(', '):
                if parameter_name.lower() in ["screen"]:
                    if re.fullmatch(r'\s*\d+(.\d+)?\s*("|inch)\s*', value.lower()):
                        parameter["values"].add(value.strip())
                else:
                    parameter["values"].add(value.strip())
        parameter["values"].add("Other")
        parameter["values"] = list(parameter["values"])
        parameter["values"].sort()
        parameters.append(parameter)
    
    return parameters

def to_int(x, default_value = 0):
    if x:
        x = int(x);
    else:
        x = default_value
    return x

def filter_product(table_name: str, filters = {}, page_index: int = 0, product_per_page: int = 20, sort_type = 0):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="crawl_database"
    )
    cursor = db.cursor()
    if not page_index or page_index < 0:
        page_index = 0
    if not product_per_page or product_per_page < 0:
        product_per_page = 20;
    if not filters:
        filters = {}
    if sort_type not in [0, 1, 2]:
        sort_type = 0
    
    sql = f"""
    SELECT name, price, url, image_path, website
    FROM {table_name}
    WHERE name IS NOT NULL AND price IS NOT NULL AND url IS NOT NULL
    """
    # loop through all filters
    condition_sql = []
    filter_choices = []
    for filter_name, filter  in filters.items():
        if not filter:
            continue
        condition_in_filter = []
        for requiredment in filter:
            if requiredment.lower() != 'other':
                requiredment = requiredment.replace(" ", "%")
                condition_in_filter.append(f"{str(filter_name).replace(' ','_')} LIKE %s")
                filter_choices.append(f"%{requiredment}%")
            else:
                condition_in_filter.append(f"{str(filter_name).replace(' ','_')} IS NULL")
        condition_sql.append(f'({" OR ".join(condition_in_filter)})')

    if condition_sql:
        sql += "AND" + " AND ".join(condition_sql)

    if sort_type == 1:
        sql += " ORDER BY price"
    elif sort_type == 2:
        sql += " ORDER BY price DESC"
    cursor.execute(sql, filter_choices)
    rows = cursor.fetchall()
    product_info = {
        "total": len(rows),
        "category": table_name.replace("_", " "),
        "listproduct": None,
    }
    start_index = min(len(rows), page_index * product_per_page)
    end_index = min(len(rows), start_index + product_per_page)

    listproduct = []
    for row in rows[start_index:end_index]:
        product = {
            "name": row[0],
            "price": '{:0,}'.format(row[1]).replace(",", ".") + " đ", 
            "url": row[2],
            "image_path": row[3],
            "website": row[4],
        }
        listproduct.append(product)
    # product_info["listproduct"] = listproduct
    product_info["listproduct"] = render_template("product_layout.html", listproduct=listproduct)
    return product_info