from flask import Flask, render_template
import folium

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
	m = folium.Map(location=[45.5236, -122.6750])
	m
	return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
