from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

# Pet model
class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String, nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)

# Add Pet form
class AddPetForm(FlaskForm):
    name = StringField("Pet Name", [validators.InputRequired()])
    species = StringField("Species", [validators.InputRequired(), validators.AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField("Photo URL", [validators.Optional(), validators.URL()])
    age = IntegerField("Age", [validators.Optional(), validators.NumberRange(min=0, max=30)])
    notes = StringField("Notes", [validators.Optional()])

# Edit Pet form
class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", [validators.Optional(), validators.URL()])
    notes = StringField("Notes", [validators.Optional()])
    available = BooleanField("Available")

# Routes
@app.route('/')
def list_pets():
    pets = Pet.query.all()
    return render_template('pets_list.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        pet = Pet(name=form.name.data, species=form.species.data, photo_url=form.photo_url.data, age=form.age.data, notes=form.notes.data)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('list_pets'))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('list_pets'))
    return render_template('edit_pet.html', form=form, pet=pet)

if __name__ == '__main__':
    app.run(debug=True)
