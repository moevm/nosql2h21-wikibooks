import os

from DBMS import DBMS
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

headings = ("Wikibooks", "Links")
list_of_lang = ("de", "en", "es", "fr", "he", "hu", "it", "ja", "nl", "pl", "pt", "ru")
db = DBMS()


# Костыль, так как IDE перезапускает код и база данных дублируется в саму себя.
def load_db(data):
    db.DELETE_ALL_RELATIONSHIPS()
    db.DELETE_NODES()
    for i in list_of_lang:
        data.print_language(i)
    for j in list_of_lang:
        data.add_book(j)
    return data


load_db(db)


@app.route('/')
def main():
    books = list(db.get_book('en'))
    return render_template("main.html", headings=headings, data=books)


@app.route('/<string:lang>', methods=["POST", "GET"])
def anotherLanguage(lang):
    books = list(db.get_book(lang))

    if request.method == "POST":
        lang = request.form['name']
        return redirect(f'/{lang}')

    return render_template('main.html', headings=headings, data=books)


@app.route('/search', methods=["GET"])
def search():
    text = request.args.get('search_text')
    print(text)
    data = []

    for i in list_of_lang:
        for j in db.get_book(i):
            data.append(j)
    res = ''

    if text:
        text = text.lower()
        res = list(filter(lambda elem: text in elem.get("a.title").lower(), data))
    return render_template('main.html', data=res)


@app.route('/import')
def dataImport():
    return render_template('import.html')


@app.route('/export')
def dataExport():
    return render_template('export.html')


@app.route('/export')
def auth():
    return render_template('auth.html')


@app.route('/export')
def stats():
    return render_template('stats.html')



#TODO
# Не работает, так как криво определяется путь до директории

# @app.route('/<string:title>')
# def mirrorPage(title, lang):
#     if request.method == "POST":
#         data = db.get_book(lang)

#         for el in data:
#           if el.get('a.title') == title:
#             match_data = el.get('a.html')
#             f_name = str(title) + '.html'
#            # directory = os.getcwd()
#
#             fo = open(r"C:\Users\nosql2h21-wikibooks\\" + "templates" + f_name, 'w')
#             fo.write(match_data)
#             fo.close()
#             print(match_data)
#             return render_template(match_data)
#           else:
#             print('error')


if __name__ == "__main__":
    app.run(debug=True)

