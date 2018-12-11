from app import create_app, db, cli
from app.models import User, Post
# import command enhancement
# from app import cli

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)