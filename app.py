from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.play import Playlist
from models.user import User

from routes.play import main as routes_play


app = Flask(__name__)
db_path = 'play.sqlite'
manager = Manager(app)

@app.errorhandler(404)
def error404(e):
    """
    自定义 404 界面
    """
    return render_template('404.html')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    # url_prefix='/todo'
    app.register_blueprint(routes_play)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()


# 第一次初始化数据库
# python3 app.py db init
# python3 app.py db migrate
# python3 app.py db upgrade

# gunicorn 运行程序
# gunicorn -b '0.0.0.0:80' redischat:app
# nohup gunicorn -b '0.0.0.0:80' redischat:app &