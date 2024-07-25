from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import PyPDF2
from gtts import gTTS
print("HEllllooooooooooo")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['AUDIO_FOLDER'] = 'audiobooks'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    print("not path")
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['AUDIO_FOLDER']):
    print("no path 2")
    os.makedirs(app.config['AUDIO_FOLDER'])

@app.route('/')
def index():
    print("hello html")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Form submitted")
    if 'pdfFile' not in request.files:
        print("No file part in request")
        return redirect(request.url)
    
    file = request.files['pdfFile']
    
    if file.filename == '':
        print("No file selected")
        return redirect(request.url)
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print(f"File saved to {file_path}")
        
        # Convert PDF to text
        pdf_reader = PyPDF2.PdfReader(open(file_path, 'rb'))
        pdf_text = ''
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()
        # print(f"Extracted text: {pdf_text[:100]}...")  # Print the first 100 characters for debugging
        print("got_text")
        
        # Convert text to speech
        tts = gTTS(text=pdf_text, lang='en')
        audio_filename = file.filename.rsplit('.', 1)[0] + '.mp3'
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        tts.save(audio_path)
        print(f"Audio file saved to {audio_path}")
        
        return render_template('index.html', audio_url=url_for('get_audio', filename=audio_filename))

    print("File not processed")
    return redirect(request.url)

@app.route('/audiobooks/<filename>')
def get_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
