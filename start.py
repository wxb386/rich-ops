#!/usr/bin/python3

from flask import request, Flask, render_template, url_for

app = Flask(
    __name__,
)

#给Flask视图加装饰器
#1、定义1个装饰器
def auth(func):
    print('我在上面')
    def inner(*args,**kwargs):
        print(args)
        print(kwargs)
        return func(*args,**kwargs)
    return inner

@app.route("/", methods=["GET"])
@auth
def hello():
    return render_template("login.html", abc="hello world!")


@app.route('/<float:url>', endpoint='name1')
def first_flask(url):
    # 如果设置了url参数，url_for（别名,加参数）
    print(url,type(url))
    print(url_for('name1', url=url))
    return "反向??不明白 %s" % url


@app.route("/login", methods=["GET"])
def login():
    return render_template("login_secc.html", content=request.args.get("username"))


@app.errorhandler(500)
def err_500(e):
    return render_template("500.html", err=e)


@app.errorhandler(404)
def err_404(e):
    return render_template("404.html", err=e)


if __name__ == '__main__':
    app.run()
