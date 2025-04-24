
from flask import Flask, render_template_string, request
import json
import os

app = Flask(__name__)

VOUCHER_FILE = 'vouchers.json'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='it'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Validazione Voucher</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; padding: 2rem; text-align: center; }
        input, button { padding: 0.5rem; font-size: 1rem; }
        #result { margin-top: 1rem; font-size: 1.2rem; font-weight: bold; }
        .valid { color: green; }
        .invalid { color: red; }
    </style>
</head>
<body>
    <h1>Validazione Voucher</h1>
    <form method="post">
        <input type="text" name="code" placeholder="Inserisci il codice voucher" required />
        <button type="submit">Verifica</button>
    </form>
    {% if result is not none %}
        <div id="result" class="{{ 'valid' if valid else 'invalid' }}">
            {{ result }}
        </div>
    {% endif %}
</body>
</html>
"""

def load_vouchers():
    if not os.path.exists(VOUCHER_FILE):
        return {}
    with open(VOUCHER_FILE, 'r') as f:
        return json.load(f)

def save_vouchers(vouchers):
    with open(VOUCHER_FILE, 'w') as f:
        json.dump(vouchers, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def validate():
    result = None
    valid = False
    if request.method == 'POST':
        code = request.form.get('code').strip()
        vouchers = load_vouchers()

        if code in vouchers:
            if not vouchers[code]['used']:
                result = "✅ Voucher valido!"
                valid = True
                vouchers[code]['used'] = True
                save_vouchers(vouchers)
            else:
                result = "❌ Voucher già utilizzato."
        else:
            result = "❌ Voucher non valido."

    return render_template_string(HTML_TEMPLATE, result=result, valid=valid)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
