from flask import Flask, render_template, send_from_directory
import os
import json

app = Flask(__name__)

MEDICAL_DIR = os.path.join(app.root_path, 'static', 'medical')
RECORDS_META = os.path.join(app.root_path, 'static', 'medical', 'records.json')

def get_records():
    """Load medical record metadata, falling back to auto-detect images."""
    # Try metadata file first
    if os.path.exists(RECORDS_META):
        try:
            with open(RECORDS_META) as f:
                return json.load(f)
        except:
            pass
    # Auto-detect images in /static/medical/
    records = []
    if os.path.exists(MEDICAL_DIR):
        exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        files = sorted([
            fn for fn in os.listdir(MEDICAL_DIR)
            if fn.lower().endswith(exts)
        ])
        for i, fn in enumerate(files, 1):
            records.append({
                'url': f'/static/medical/{fn}',
                'label': f'Medical Record {i}',
                'note': ''
            })
    return records


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr')
def qr():
    return send_from_directory('static', 'qr_document.html')

@app.route('/medical')
def medical():
    records = get_records()
    return render_template('medical.html', records=records)

@app.route('/static/medical/<path:filename>')
def medical_file(filename):
    return send_from_directory(MEDICAL_DIR, filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
