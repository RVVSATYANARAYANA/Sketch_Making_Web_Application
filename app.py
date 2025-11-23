import cv2
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED = {"png", "jpg", "jpeg"}

def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED

def make_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return sketch

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sketch", methods=["POST"])
def sketch():
    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        img = cv2.imread(path)
        sketch_img = make_sketch(img)

        sketch_name = filename.rsplit(".", 1)[0] + "_sketch.jpg"
        sketch_path = os.path.join(app.config["UPLOAD_FOLDER"], sketch_name)
        cv2.imwrite(sketch_path, sketch_img)

        return render_template("home.html",
                               org_img_name=filename,
                               sketch_img_name=sketch_name)

    return "Invalid file"

if __name__ == "__main__":
    app.run(debug=True)
