from apps import create_app, db
from apps.routes.default_categories import add_default_categories
app = create_app()

@app.before_request
def create_tables():
    db.create_all()
    add_default_categories()
  

if __name__ == '__main__':
    app.run(debug=True)