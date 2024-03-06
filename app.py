from flask import Flask, jsonify, abort, make_response, request, redirect, url_for, render_template
from models import liblary
from forms import LiblaryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "ninini"

@app.route("/api/v1/liblary/", methods=["GET"])
def liblary_list_api_v1():
    return jsonify(liblary.all())

@app.route("/api/v1/liblary/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = liblary.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})

@app.route("/api/v1/liblary/", methods = ['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id' : liblary.all()[-1]['id'] + 1,
        'title' : request.json['title'],
        'book_color' : request.json.get('book_color', ""),
        'page_number' : request.json.get('page_number', ""),
        'shelf' : False
    }
    liblary.create(book)
    return jsonify({'book' : book}), 201

@app.route("/api/v1/liblary/<int:book_id>", methods = ['DELETE'])
def delete_book(book_id):
    result = liblary.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result' : result})

@app.route("/api/v1/liblary/<int:book_id>")
def update_book(book_id):
    book = liblary.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)

    data = request.json
    
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'book_color' in data and not isinstance(data.get('book_color'), str),
        'page_number' in data and not isinstance(data.get('page_number'), int),
        'shelf' in data and not isinstance(data.get('shelf'), bool)
    ]):
        abort(400)
    book = {
        'title' : data.get('title', book['title']),
        'book_color' : data.get('book_color', book['book_color']),
        'page_number' : data.get('page_number', book['page_nnumber']),
        'shelf' : data.get('shelf', book['shelf'])
    }
    liblary.update(book_id, book)
    return jsonify({'book' : book})

@app.route("/liblary/", methods = ['GET', 'POST'])
def liblary_list():
    form = LiblaryForm()
    error = ""

    if request.method == 'POST':
        if form.validate_on_submit():
            liblary.create(form.data)
            liblary.save_all()
        return redirect(url_for("liblary_list"))
    return render_template("liblary.html", form=form, error=error, liblary=liblary.all())

@app.route("/liblary/<int:book_id>", methods = ['POST', 'GET'])
def liblary_details(book_id):
    book = liblary.get(book_id - 1)
    form = LiblaryForm(data = book)

    if request.method == 'POST':
        if form.validate_on_submit():
            liblary.update(book_id - 1, form.data)
        return redirect(url_for("liblary_list"))
    return render_template("book.html", form=form, book_id=book_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error' : 'Bad request', 'status_code' : 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)