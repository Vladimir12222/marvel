from flask import Flask, render_template, g, request, flash, redirect, url_for
import sqlite3
import math
import time


app = Flask(__name__)

app.config["SECRET_KEY"] = "Asd3GSDgL437)tjnhFDsj!cljW4hcJ"
menu = [
            {"name": "About", "link": "about"},
            {"name": "Projects", "link": "project"},
            {"name": "Resume", "link": "resume"},
            {"name": "Contact", "link": "contact"}
        ]
owner = {"surname": "Vladimir",
         "phone": "+7(999)877-87-87",
         "email": "test.testovich@mail.ru",
         "anim_item": ['Smirnov Vladimir',
                       'Python developer',
                       'UI Specialist', ],
         "social_links": [{"name": "Dribbble", "link": "#"},
                          {"name": "Instagram", "link": "#"},
                          {"name": "Youtube", "link": "#"}]
         }

designer = {"name": "Smirnov Vladimir",
            "company_name": "RAY Company",
            "year": "2024"}

project_foto = [{"path": "/static/images/project/project-image01.png"},
                {"path": "/static/images/project/project-image02.png"},
                {"path": "/static/images/project/project-image03.png"},
                {"path": "/static/images/project/project-image04.png"},
                {"path": "/static/images/project/project-image05.png"},
                ]

experiences = [
    {"year": "2019", "profession": "Project Manager", "company": "Best Studio",
     "comment": "Proin ornare non purus ut rutrum. Nulla facilisi. Aliquam laoreet libero ac "
                "pharetra feugiat. Cras ac fermentum nunc, a faucibus nunc."},
    {"year": "2018", "profession": "UX Designer", "company": "Digital Ace",
     "comment": "Fusce rutrum augue id orci rhoncus molestie. Nunc auctor dignissim lacus vel iaculis."},
    {"year": "2016", "profession": "UI Freelancer", "company": "",
     "comment": "Sed fringilla vitae enim sit amet cursus. Sed cursus dictum tortor quis pharetra. Pellentesque "
                "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."},
    {"year": "2014", "profession": "Junior Designer", "company": "Crafted Co.",
     "comment": "Cras scelerisque scelerisque condimentum. Nullam at volutpat mi. Nunc auctor ipsum eget magna "
                "consequat viverra."},
]

educations = [{"year": "2017", "item": "Mobile Web", "where": "Master Design",
               "comment": "Please tell your friends about Tooplate website. That would be very helpful. We need your "
                          "support."},
              {"year": "2015", "item": "User Interfaces", "where": "Creative Agency", "site": "https://www.facebook"
                                                                                              ".com/tooplate",
               "namesite": "Tooplate",
               "comment": "is a great website to download HTML templates without any login or email."},
              {"year": "2013", "item": "Artwork Design", "where": "New Art School",
               "comment": "You can freely use Tooplate's templates for your business or personal sites. You cannot "
                          "redistribute this template without a permission."},
              ]


def connect_db():
    connection = sqlite3.connect('my_database.db')
    return connection


def create_db():
    db = connect_db()
    with app.open_resource("db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.route('/', methods=['GET', 'POST'])
def hello():
    create_db()
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['message']) > 10:
            res = (request.form['name'], request.form['email'], request.form['message'])
            if not res:
                flash("Ошибка добавления", category="error")
            else:
                flash("Успешно добавлено", category="success")
        else:
            flash("Ошибка добавления, проверьте ваши данные", category="error")
            return redirect(url_for('hello'))
        try:
            db = get_db()
            cur = db.cursor()
            tm = math.floor(time.time())
            cur.execute("INSERT INTO posts VALUES (NULL,?,?,?,?)", (res[0], res[1], res[2], tm))
            db.commit()
            return redirect(url_for('hello'))
        except:
            print("Error adding post")
    return render_template('/index.html', menu=menu, owner=owner, project_foto=project_foto, experiences=experiences,
                           educations=educations, designer=designer)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)