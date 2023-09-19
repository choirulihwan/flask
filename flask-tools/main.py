import os
from pathlib import Path

from flask import Flask, request, flash, redirect, url_for, current_app, send_file
from flask import render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'webp', 'png'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/download/<name>', methods=['GET', 'POST'])
def download_file(name):
    path = os.path.join(current_app.root_path, app.config['OUTPUT_FOLDER'], name)
    return send_file(path, as_attachment=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# pdf to excel
@app.route("/toexcel", methods=['GET', 'POST'])
def toexcel():
    if request.method == 'POST':
        import subprocess

        if 'filepdf' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filepdf']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            filename_only = Path(file_path).stem
            file.save(file_path)

            # convert to excel
            file_output = os.path.join(app.config['OUTPUT_FOLDER'], filename_only + ".csv")
            import tabula
            df = tabula.read_pdf(input_path=file_path, pages="all")
            tabula.convert_into(input_path=file_path, output_path=file_output, output_format="csv", pages="all", stream=True)

            return redirect(url_for('download_file', name=filename_only + ".csv"))
    else:
        return render_template('pdf_to_excel.html')


# image module
@app.route("/removebg", methods=['GET', 'POST'])
def removebg():

    if request.method == 'POST':
        from rembg import remove
        from PIL import Image

        if 'file_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file_image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_image(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            input_path = file_path
            filename_only = Path(file_path).stem
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename_only + ".png")

            input2 = Image.open(input_path)
            output = remove(input2)
            output.save(output_path)

            flash('Process finished')
        # return render_template('remove_background.html', data=output_path)
        return redirect(url_for('download_file', name=filename_only + ".png"))
    else:
        return render_template('remove_background.html')


# socmed module
def on_complete(filename):
    flash('Video Downloaded')


@app.route("/youtubedownloader", methods=['GET', 'POST'])
def youtubedownloader():
    if request.method == 'POST':
        import pytube

        link = request.form['link']
        args = link.split("=")

        filename = args[1] + '.mp4'
        yt = pytube.YouTube(link, on_complete_callback=on_complete(filename))
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        video.download(app.config["UPLOAD_FOLDER"], filename)

        return render_template('youtube_downloader.html', data=link, filename=filename)
    else:
        return render_template('youtube_downloader.html')


# code module
@app.route("/barcode", methods=['GET', 'POST'])
def barcode():
    if request.method == 'POST':
        from barcode import Code128

        data = request.form['barcode']

        code = Code128(data)
        code.save("output/barcode" + data)
        flash('Barcode generated')

        # return render_template('barcode.html', data=data)
        return redirect(url_for('download_file', name="barcode" + data + ".svg"))
    else:
        return render_template('barcode.html')


# pdf module
@app.route("/compresspdf", methods=['GET', 'POST'])
def compresspdf():
    if request.method == 'POST':
        import subprocess


        if 'filepdf' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filepdf']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            filename_only = Path(file_path).stem
            file.save(file_path)

            # command = "pdf-compressor --set-api-key project_public_4e17bb4c23b0564a11aa32e4083d540b_FRs-P26c5625064d0e2e6462071e8834d71d6"
            # try:
            #     result = subprocess.run(command, shell=True)
            # except subprocess.CalledProcessError as e:
            #     return "Error on API."

            command2 = "pdf-compressor {0}".format(file_path)
            try:
                result = subprocess.run(command2, shell=True)
            except subprocess.CalledProcessError as e:
                return "Error on Compress"

            filename_only = filename_only + "-compressed.pdf"
            return redirect(url_for('download_file', name=filename_only))
    else:
        return render_template('pdf.html')
