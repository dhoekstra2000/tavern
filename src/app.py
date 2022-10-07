import connexion

app = connexion.FlaskApp(__name__, specification_dir="tavern/openapi/")
app.add_api("api.yaml")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
