import re
from flask import Blueprint, render_template, redirect, request, make_response, flash
from services import users

controller = Blueprint("users", __name__)


@controller.route("/login", methods=["POST"])
def post_login_data():
    user_id = request.form.get("username")
    password = request.form.get("password")
    print(user_id)
    print(password)

    # 로그인 성공
    if users.verify_user(user_id, password):
        # not "/my", "my". "my" == "/users/my", "/my" = "/my"
        res = make_response(redirect("my"))
        res.set_cookie("user_id", user_id)
        return res
    else:
        flash("로그인 실패. 다시 시도하세요")
        return redirect("/")


@controller.route("/logout", methods=["GET"])
def logout():
    res = make_response(redirect("/"))
    res.delete_cookie("user")
    return res


@controller.route("/my", methods=['GET'])
def mypage():
    # 쿠키가 있다 -> 로그인된 유저라면
    user_id = request.cookies.get("user_id")
    print('user_id:', user_id)
    user = users.get_user_by_id(user_id)
    if user:  # 로그인 된 경우
        return render_template("my.html", user=user)
    else:
        flash("로그인되지 않았습니다")
        return redirect("/")


@controller.route("/signup", methods=["GET"])
def sign_up_form():
    return render_template("sign_up.html")

@controller.route("/signup", methods=["POST"])
def sign_up():
    print(request.form)
    data = request.form

    # check validation by
    valid_password = re.fullmatch('/^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]|.*[0-9]).{8,24}$/', data["password"])
    valid_birth = re.fullmatch('', data["birth"])
    valid_phonenumber = re.fullmatch('/^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$/', data["birth"])

    if not (valid_password):
        flash("비밀번호는 8~24자 영문대소문자, 숫자, 특수문자 혼합 사용해야합니다.")
        return render_template("back.html")

    if not (valid_birth):
        flash("생년월일 형식이 알맞지 않습니다. YYYYMMDD")
        return render_template("back.html")

    if not (valid_phonenumber):
        flash("전화번호 형식이 알맞지 않습니다. XXX-XXXX-XXXX")
        return render_template("back.html")

    # [{'InsertNewUserErrorMessage': 'User ID already exists.'}]
    # [{'InsertNewUserSuccessMessage': 'Insert new User successfully'}]
    # log_type = log[0].keys()[0]
    # log_value = log[0].items()[0]
    # print(log_type, log_value)

    log = users.sign_up(data["id"], data["password"], data["name"], data["birth"], data["phonenumber"], data["gender"], data["address"], data["role"])
    print(log)
    flash(log)



    return redirect("/")
