from flask import Flask, render_template
from data import db_session
from data.constants import DB_NAME
from data.news import News
from data.users import User
from data.forms import RegisterForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template("register.html", title="Регистрация",
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return "Вы успешно зарегистрированы!"
    return render_template("register.html", title="Регистрация", form=form)


def main():
    db_session.global_init(DB_NAME)
    app.run()


if __name__ == "__main__":
    main()
