from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os
import validators
from tkinter import Tk
from tkinter.filedialog import askdirectory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        if not validators.url(url):
            raise ValueError('Invalid URL')

        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        filename = video.title + '.mp4'

        # Opens a file dialog to select a directory
        root = Tk()
        root.withdraw()
        directory = askdirectory()

        # Saves the file in the selected directory
        filepath = os.path.join(directory, filename)
        stream.download(output_path=directory, filename=filename)

        return send_file(filepath, as_attachment=True, attachment_filename=filename)

    except ValueError as e:
        message = str(e)
        return render_template('result.html', message=message)

    except Exception as e:
        message = 'An error occurred: {}'.format(str(e))
        return render_template('result.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
