from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/')
def root():
    print(request.headers)
    return render_template('index.html')

@app.route('/message/<my_message>')
def message(my_message):
    return render_template('message.html', message=my_message)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
