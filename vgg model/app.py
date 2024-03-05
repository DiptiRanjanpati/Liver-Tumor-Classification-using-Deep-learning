from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load your pre-trained model
model = load_model('model/vgg16tumor.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.
    return img

def get_tumor_percentage(prediction):
    # Convert prediction to percentage
    return round(prediction * 100, 2)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            processed_image = preprocess_image(file_path)
            prediction = model.predict(processed_image)
            # Customize this part based on your model's output
            if prediction[0][0] > 0.5:
                result = "Cholangiocarcinoma"
                percentage = get_tumor_percentage(prediction[0][0])
            else:
                result = "HCC (Hepatocellular Carcinoma)"
                percentage = get_tumor_percentage(1 - prediction[0][0])
            return render_template('index.html', filename=filename, result=result, percentage=percentage)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
