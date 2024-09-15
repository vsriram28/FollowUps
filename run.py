from app import app
from app.routes import users, meetings, notes, followups, tenants, home

if __name__ == '__main__':
    app.run(debug=True)
    #  app.run(host='127.0.0.1', port=5001, debug=True)
