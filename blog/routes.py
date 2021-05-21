# blog/routes.py

from faker import Faker
from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
    #generate fake entries once
    #generate_entries()
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
   form = EntryForm()
   return handle_entry(request.method, form, None)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
   entry = Entry.query.filter_by(id=entry_id).first_or_404()
   form = EntryForm(obj=entry)
   return handle_entry(request.method, form, entry)

def handle_entry(method, form, entry):
    errors = None
    if method == 'POST':
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
            else:
                entry = Entry(
                title = form.title.data,
                body = form.body.data,
                is_published = form.is_published.data
                )
                db.session.add(entry)
            db.session.commit()
        else:
           errors = form.errors
    return render_template("entry_form.html", form = form, errors = errors)



def generate_entries(how_many=10):
   fake = Faker()
   for i in range(how_many):
       post = Entry(
           title=fake.sentence(),
           body='\n'.join(fake.paragraphs(15)),
           is_published=True
       )
       db.session.add(post)
   db.session.commit()
