from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

texts = ["Donec eget mattis nunc. Donec dui mi, eleifend sed semper ut, dictum nec odio. Fusce eu nisi et lacus ultricies venenatis. Donec nibh diam, porttitor et arcu vitae, gravida venenatis purus. Mauris viverra aliquam justo sed mattis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis aliquam neque consectetur lorem maximus, ac mattis erat ornare.",
"Maecenas a felis eu quam laoreet auctor. Aliquam iaculis porta lectus. Vivamus accumsan vel ipsum maximus feugiat. Aliquam mattis tempor placerat. Praesent in magna quis metus posuere posuere. Pellentesque facilisis nulla id dui finibus, ac euismod lorem consequat. Morbi vulputate porttitor nulla blandit euismod. Donec tempor at enim vel ultrices.",
"Fusce nulla nunc, porttitor vitae nibh ac, dignissim egestas orci. Proin fringilla aliquam laoreet. Etiam sollicitudin pulvinar fringilla. Phasellus eu eros ac metus ultricies egestas. In mattis quam quis sagittis malesuada. Morbi pharetra id leo quis viverra. Phasellus quis accumsan nulla. Mauris feugiat, magna et fringilla ullamcorper, ligula purus laoreet elit, sed venenatis lorem mauris nec ligula."]

@app.route("/first")
def first():
    return texts[0]

@app.route("/second")
def second():
    return texts[1]

@app.route("/third")
def third():
    return texts[2]
