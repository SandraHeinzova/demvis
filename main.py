from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap5
from sqlalchemy import select, func
from models import Meal, User, db, UserPreferences
# from models import dummy_records
from forms import LoginForm, NewMealForm, RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "my-secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demvis.db'
db.init_app(app)

with app.app_context():
    db.create_all()
    # db.session.add_all(dummy_records)
    # db.session.commit()

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Pro zobrazení této stránky se musíš přihlásit."


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            flash("Tuto stránku nemůžeš zobrazit. ")
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("index.html", active_page="home")


@app.route("/generator")
def generator():
    return render_template("generator.html", active_page="generator")


@app.route("/add_new", methods=["POST", "GET"])
@login_required
def add_new():
    form = NewMealForm()
    if request.method == "POST":
        new_meal = Meal(name=form.data.get("name"),
                        meat=form.data.get("meat"),
                        vegetarian=True if form.data.get("vegetarian") == "Ano" else False,
                        active=False)
        db.session.add(new_meal)
        db.session.commit()
        flash("Úspěšně přidáno", "success")
        return redirect(url_for('add_new'))
    return render_template("add_new.html", active_page="add_new", form=form)


@app.route("/menu_example")
def menu_example():
    meals = db.session.execute(
        select(Meal).order_by(func.random()).limit(1).where(Meal.active == True)).scalars().all()
    return render_template("menu.html", meal_list=meals)


@app.route("/menu")
@login_required
def menu():
    value = request.args.get("value")
    meals = db.session.execute(
        select(Meal).order_by(func.random()).limit(int(value)).where(Meal.active == True)).scalars().all()
    return render_template("menu.html", meal_list=meals)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.data.get("email")
            result = db.session.execute(select(User).where(User.email == email))
            user = result.scalar()
            if user:
                flash("Účet s tímto emailem je již zaregistrován. Přihlaš se.", "warning")
                return redirect(url_for("login"))
            else:
                hash_and_salted_password = generate_password_hash(
                    form.data.get("password"),
                    method="pbkdf2:sha256",
                    salt_length=8
                )

                new_user = User(username=form.data.get("username"),
                                password=hash_and_salted_password,
                                email=email)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                next_page = request.args.get("next")
                return redirect(next_page or url_for("generator"))
    return render_template("register.html", active_page="login", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.data.get("email")
            password = form.data.get("password")
            result = db.session.execute(select(User).where(User.email == email))
            user = result.scalar()
            if not user or not check_password_hash(user.password, password):
                flash("Email neexistuje nebo špatné heslo. Prosím zkus to znovu.")
                return redirect(url_for("login"))
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("generator"))
    return render_template("login.html", active_page="login", form=form)


@app.route("/contact")
def contact():
    return render_template("contact.html", active_page="contact")


@app.route('/activate_record/', methods=['POST'])
@admin_only
def activate_record():
    action = request.form.get("action")
    record_id = request.form.get('record_id')
    record = db.session.execute(select(Meal).where(Meal.id == record_id)).scalar()
    if action == "activate":
        record.active = True

    elif action == "edit":
        record.name = request.form.get("name")
        record.meat = request.form.get("meat")
        record.vegetarian = False if request.form["vegetarian"] == "False" else True
        record.active = True

    elif action == "delete":
        db.session.delete(record)

    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        vegetarian = "only_vegetarian" in request.form
        beef = "no_beef" in request.form
        chicken = "no_chicken" in request.form
        pork = "no_pork" in request.form

        preferences = db.session.query(UserPreferences).filter_by(user_id=current_user.id).first()

        if not preferences:
            preferences = UserPreferences(user_id=current_user.id)
            db.session.add(preferences)

        preferences.vegetarian = vegetarian
        preferences.no_beef = beef
        preferences.no_chicken = chicken
        preferences.no_pork = pork
        db.session.commit()

        return redirect(url_for("profile"))

    preferences = db.session.query(UserPreferences).filter_by(user_id=current_user.id).first()
    return render_template("profile.html", active_page="profile", preferences=preferences)


@app.route("/admin")
@admin_only
def admin():
    waiting_records = db.session.execute(
        select(Meal).where(Meal.active == False)).scalars().all()
    return render_template("admin.html", waiting_records=waiting_records, active_page="admin")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Úspěšně odhlášeno!", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=3000)
