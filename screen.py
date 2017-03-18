import flask
from io import BytesIO
import logging
import os
import pyscreenshot
import sys

if os.name == "nt":
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

app = flask.Flask(__name__)


@app.route('/screen.png')
def serve_pil_image():
    quality = flask.request.args.get("quality", 10)
    extension = flask.request.args.get("extension", "jpeg")
    img_buffer = BytesIO()
    pyscreenshot.grab().save(img_buffer, extension.upper(),
                             quality=int(quality))
    img_buffer.seek(0)
    return flask.send_file(img_buffer,
                           mimetype='image/%s' % extension)


@app.route('/')
def serve_img():
    return flask.render_template('screen.html')


if __name__ == "__main__":
    argv = dict(enumerate(sys.argv))
    port = int(argv.get(1, 5000))
    logging_level = argv.get(2, "NOTSET")
    debug = argv.get(3) != "False"

    logging.getLogger("werkzeug").setLevel(logging_level)

    app.run(host='0.0.0.0', port=port, debug=debug)
