import qrcode
import io
import base64
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- HTML & CSS TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Code Generator</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f8f9fa; text-align: center; margin-top: 50px; }
        .container { display: inline-block; padding: 30px; background: white; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); width: 400px; }
        input[type="text"] { width: 80%; padding: 10px; margin: 15px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        button { width: 84%; background-color: #6f42c1; color: white; border: none; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #59359a; }
        .qr-box { margin-top: 25px; padding: 15px; background: #e9ecef; border-radius: 5px; }
        img { max-width: 200px; margin-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <h2>📷 QR Code Generator</h2>
    <p>Convert any Text or URL into a QR Code</p>
    <form method="POST">
        <input type="text" name="qr_data" placeholder="Enter text or URL here" required>
        <button type="submit">Generate QR Code</button>
    </form>

    {% if qr_img_base64 %}
        <div class="qr-box">
            <h3>Your Generated QR Code:</h3>
            <!-- Displaying Image Generation concept output directly on browser -->
            <img src="data:image/png;base64,{{ qr_img_base64 }}" alt="QR Code">
        </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def generate_qr():
    qr_img_base64 = None

    if request.method == 'POST':
        data_to_encode = request.form.get('qr_data')
        
        # Library Use Concept: Utilizing the qrcode library
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data_to_encode)
        qr.make(fit=True)
        
        # Image Generation Concept: Creating the image object
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Saving image in buffer memory to stream on browser without saving physically
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template_string(HTML, qr_img_base64=qr_img_base64)

if __name__ == '__main__':
    app.run(debug=True)
