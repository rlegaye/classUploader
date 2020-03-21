from flask import Flask, request, render_template
from datetime import datetime
import requests
import cloudinary
import cloudinary.uploader

cameraUrl = "http://10.192.101.171"

cloudinary.config(
    cloud_name = "djpspvb4v",
    api_key = "672854352616411",
    api_secret = "9LJCHQOGarWstgEWY6BKx7JeoGM"
)

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

@upload_app.route('/upload')
def upload_form():
    return render_template('upload.html')

@upload_app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


upload_app.run(host='0.0.0.0', port=5000)