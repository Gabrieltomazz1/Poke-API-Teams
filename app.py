from config import app, db
from routes.pokemon import router

app.register_blueprint(router)


def create_app_context():
    return app.app_context()


if __name__ == "__main__":
    with create_app_context():
        #     try:
        #         Owner.table
        #         Pokemon.table
        #         Team.__table
        #     except Exception as e:
        db.create_all()
        db.session.commit()
    app.run("0.0.0.0", debug=True)
