from flask import Flask, request, render_template, flash, redirect
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import os
import requests
import cloudinary
import cloudinary.uploader


upload_app = Flask(__name__)

UPLOAD_FOLDER = './'
upload_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_app.secret_key = '0TzSee3w8i'


cameraUrl = "http://10.192.101.171"

cloudinary.config(
    cloud_name = "djpspvb4v",
    api_key = "672854352616411",
    api_secret = "9LJCHQOGarWstgEWY6BKx7JeoGM"
)

ALLOWED_EXTENSIONS = set(['mov', 'mp4', 'png', 'jpg', 'jpeg', 'gif'])

auth = HTTPBasicAuth()

users = {
    "charli": generate_password_hash("Covid19!"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def printing_something(text):
    print("printing %s at %s" % (text, datetime.now()))

def record_class(className, duration, preset):
    URL = cameraUrl + "/command/presetposition.cgi"
    PARAMS = {"PresetCall":preset + ",24"}
    r = requests.get(url = URL, params = PARAMS)
    print(r)
    print("recording %s for %s seconds at %s" % (className, duration, preset))
    fileNameSansExt = className + "_" + str(datetime.now().year) + "_" + str(datetime.now().month) + "_" + str(datetime.now().day) + "_" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
    fileName = fileNameSansExt + ".mp4"
    #stream = ffmpeg.input(cameraUrl + "/image1", t=int(duration), r=30)
    #stream = ffmpeg.output(stream, fileName, r=30)
    #ffmpeg.run(stream)
    print("done recording %s for %s seconds at %s" % (className, duration, preset))
    cloudinaryRes = cloudinary.uploader.upload(fileName, resource_type = "video", public_id = fileNameSansExt);
    print(cloudinaryRes)

def upload():
    cloudinaryRes = cloudinary.uploader.upload(fileName, resource_type = "video", public_id = fileNameSansExt);

@upload_app.route('/')
@auth.login_required
def upload_form():
    return render_template('upload.html')

@upload_app.route('/', methods=['POST'])
def upload_file():
    print(request.form)
    now = datetime.now() # current date and time
    instructorFirstName = request.form['instructorFirstName']
    className = request.form['className']
    print("empty2")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if instructorFirstName == '':

            flash('No first name input for upload')
            return redirect(request.url)
        if className == '':
            flash('No class name input for upload')
            return redirect(request.url)
        #if file and allowed_file(file.filename):
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_app.config['UPLOAD_FOLDER'], filename))
            fileNameSansExt = filename.rsplit('.')[0].lower()
            date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
            #print("done recording %s for %s seconds at %s" % (className, duration, preset))
            fileNamePublic = fileNameSansExt + '_' + className + '_' + date_time
            async_option = {"async":True}
            notification_url = "https://eni5be5irqov.x.pipedream.net"
            cloudinaryRes = cloudinary.uploader.upload_large(filename, resource_type = "video", public_id = fileNamePublic, eager=[{"streaming_profile":"full_hd", "format":"m3u8"}], eager_async=True, eager_notification_url=notification_url, notification_url=notification_url, context="className=" + className + "|instructorFirstName=" + instructorFirstName, **async_option);
            os.remove(filename)
            print(cloudinaryRes)
            flash(filename + ' successfully uploaded at ' + date_time)
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


upload_app.run(host='0.0.0.0', port=5000)