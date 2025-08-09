from flask import Flask, request, render_template_string
import os, csv, re
from datetime import datetime

app = Flask(__name__)

HISTORY_PATH = "/data/history.csv"
os.makedirs("/data", exist_ok=True)

TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Flaskulator</title>
    <style>
      body { font-family: system-ui, sans-serif; max-width: 360px; margin: 2rem auto; }
      .display { width: 100%; font-size: 1.5rem; text-align: right; padding: .5rem; margin-bottom: .75rem; }
      .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .5rem; }
      button { padding: .75rem; font-size: 1.1rem; }
      .op { background: #eee; }
      .eq { background: #cde; }
      .clr { background: #f6c; }
      h2 { text-align: center; }
    </style>
  </head>
  <body>
    <h2>Flaskulator</h2>

    <form method="post">
      <input type="hidden" name="expr" value="{{ expr }}">
      <input class="display" value="{{ result if result is not none else (expr if expr else '0') }}" disabled>

      <div class="grid">
        <button name="key" value="7">7</button>
        <button name="key" value="8">8</button>
        <button name="key" value="9">9</button>
        <button class="op" name="key" value="+">+</button>

        <button name="key" value="4">4</button>
        <button name="key" value="5">5</button>
        <button name="key" value="6">6</button>
        <button class="op" name="key" value="-">-</button>

        <button name="key" value="1">1</button>
        <button name="key" value="2">2</button>
        <button name="key" value="3">3</button>
        <button class="op" name="key" value="*">*</button>

        <button name="key" value="0">0</button>
        <button name="key" value=".">.</button>
        <button class="clr" name="key" value="C">C</button>
        <button class="eq" name="key" value="=">=</button>
      </div>
    </form>
  </body>
</html>
"""

def append_history(x, op, y, result):
    first_time = not os.path.exists(HISTORY_PATH)
    with open(HISTORY_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if first_time:
            w.writerow(["when", "x", "op", "y", "result"])
        w.writerow([datetime.utcnow().isoformat(timespec="seconds") + "Z", x, op, y, result])

def compute_if_binary(expr):
    """
    Accepts 'number op number' where op in {+,-,*}.
    Returns (result, x, op, y) or (None, None, None, None).
    """
    # Note: hyphen is safe when the class is written as [-+*]
    m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*([-+*])\s*(-?\d+(?:\.\d+)?)\s*", expr or "")
    if not m:
        return None, None, None, None
    x, op, y = m.group(1), m.group(2), m.group(3)
    xf, yf = float(x), float(y)
    if op == "+":
        res = xf + yf
    elif op == "-":
        res = xf - yf
    else:
        res = xf * yf
    return res, x, op, y

@app.route("/", methods=["GET", "POST"])
def home():
    expr = request.form.get("expr", "")
    result = None

    if request.method == "POST":
        key = request.form.get("key", "")

        if key == "C":
            expr = ""
        elif key == "=":
            res, x, op, y = compute_if_binary(expr)
            if res is not None:
                result = res
                append_history(x, op, y, res)
                expr = str(res)  # keep result for next operation
        else:
            # append digit/operator/decimal with light guarding against double operators
            if key in "+-*":
                if not expr or expr[-1] in "+-*":
                    expr = (expr[:-1] if expr else "") + key
                else:
                    expr += key
            elif key == ".":
                last_op = max(expr.rfind("+"), expr.rfind("-"), expr.rfind("*"))
                segment = expr[last_op+1:] if last_op >= 0 else expr
                if "." not in segment:
                    expr += "."
            else:
                expr += key

    return render_template_string(TEMPLATE, expr=expr, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
