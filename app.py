import numpy as np
from bidict import bidict
from flask import Flask, render_template, request, session, redirect, url_for
# from flask_cors import CORS
from random import choice
from tensorflow import keras


# custom label encoder (to be used within the model).
# bidict makes reverse lookups easier
ENCODER = bidict({
    'A': 1, 'I': 2, 'U': 3, 'E': 4, 'O': 5,
    'KA': 6, 'KI': 7, 'KU': 8, 'KE': 9, 'KO': 10,
    'SA': 11, 'SHI': 12, 'SU': 13, 'SE': 14, 'SO': 15,
    'TA': 16, 'CHI': 17, 'TSU': 18, 'TE': 19, 'TO': 20,
    'NA': 21, 'NI': 22, 'NU': 23, 'NE': 24, 'NO': 25,
    'HA': 26, 'HI': 27, 'FU': 28, 'HE': 29, 'HO': 30,
    'MA': 31, 'MI': 32, 'MU': 33, 'ME': 34, 'MO': 35,
    'YA': 36, 'YU': 37, 'YO': 38,
    'RA': 39, 'RI': 40, 'RU': 41, 'RE': 42, 'RO': 43,
    'WA': 44, 'WO': 45, 'N': 46
})

CHAR_MAP = bidict({
    'あ': 'A', 'い': 'I', 'う': 'U', 'え': 'E', 'お': 'O',
    'か': 'KA', 'き': 'KI', 'く': 'KU', 'け': 'KE', 'こ': 'KO',
    'さ': 'SA', 'し': 'SHI', 'す': 'SU', 'せ': 'SE', 'そ': 'SO',
    'た': 'TA', 'ち': 'CHI', 'つ': 'TSU', 'て': 'TE', 'と': 'TO',
    'な': 'NA', 'に': 'NI', 'ぬ': 'NU', 'ね': 'NE', 'の': 'NO',
    'は': 'HA', 'ひ': 'HI', 'ふ': 'FU', 'へ': 'HE', 'ほ': 'HO',
    'ま': 'MA', 'み': 'MI', 'む': 'MU', 'め': 'ME', 'も': 'MO',
    'や': 'YA', 'ゆ': 'YU', 'よ': 'YO', 'ら':
    'RA', 'り': 'RI', 'る': 'RU', 'れ': 'RE', 'ろ': 'RO',
    'わ': 'WA', 'を': 'WO', 'ん': 'N'
})

# used for showing progress during the "full quiz".
# 0 -> unanswered, 1 -> correct, 2 -> incorrect
QUIZ_PROG = [
    ('WA', 'わ', 0), ('RA', 'ら', 0), ('YA', 'や', 0), ('MA', 'ま', 0), ('HA', 'は', 0),
    ('NA', 'な', 0), ('TA', 'た', 0), ('SA', 'さ', 0), ('KA', 'か', 0), ('A', 'あ', 0),
    ('.wi', '', 0), ('RI', 'り', 0), ('.yi', '', 0), ('MI', 'み', 0), ('HI', 'ひ', 0),
    ('NI', 'に', 0), ('CHI', 'ち', 0), ('SHI', 'し', 0), ('KI', 'き', 0), ('I', 'い', 0),
    ('WO', 'を', 0), ('RU', 'る', 0), ('YU', 'ゆ', 0), ('MU', 'む', 0), ('FU', 'ふ', 0),
    ('NU', 'ぬ', 0), ('TSU', 'つ', 0), ('SU', 'す', 0), ('KU', 'く', 0), ('U', 'う', 0),
    ('.we', '', 0), ('RE', 'れ', 0), ('.ye', '', 0), ('ME', 'め', 0), ('HE', 'へ', 0),
    ('NE', 'ね', 0), ('TE', 'て', 0), ('SE', 'せ', 0), ('KE', 'け', 0), ('E', 'え', 0),
    ('N', 'ん', 0), ('RO', 'ろ', 0), ('YO', 'よ', 0), ('MO', 'も', 0), ('HO', 'ほ', 0),
    ('NO', 'の', 0), ('TO', 'と', 0), ('SO', 'そ', 0), ('KO', 'こ', 0), ('O', 'お', 0)
]


# app set up
app = Flask(__name__)
# CORS(app)
app.secret_key = 'something_sneaky'


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/train', methods=['GET'])
def train_get():

    msg = session.get('msg', '')

    #
    #   OPTION 1:
    #       grab a character that has few instances
    #       in the training data compared to other chars
    #
    labels = np.load("data/labels.npy")
    count = {k: 0 for k in ENCODER.keys()}
    for label in labels:
        count[label] += 1
    count = sorted(count.items(), key=lambda x: x[1])
    # q = choice(count[:len(count)//4])[0]
    q = count[0][0]

    #
    #   OPTION 2:
    #       just choose a random one
    #
    # q = choice( list(ENCODER.keys()) )

    return render_template('train.html', q=q, msg=msg)


@app.route('/train', methods=['POST'])
def train_post():

    label = request.form['question']
    labels = np.load("data/labels.npy")
    labels = np.append(labels, label)

    pixels_str = request.form['pixels']
    pixels = pixels_str.split(',')
    img = np.array(pixels).astype(float).reshape(1, 50, 50)

    all_imgs = np.load("data/imgs.npy")
    all_imgs = np.vstack([all_imgs, img])

    np.save("data/labels.npy", labels)
    np.save("data/imgs.npy", all_imgs)

    session['msg'] = f'"{label}" updated in the training data'

    return redirect(url_for('train_get'))


@app.route('/practice', methods=['GET'])
def practice_get():
    return render_template('practice.html', q=choice(list(ENCODER.keys())))


@app.route('/practice', methods=['POST'])
def practice_post():
    try:
        question = request.form['question']

        pixels_str = request.form['pixels']
        pixels = pixels_str.split(',')
        img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)

        model = keras.models.load_model('kana.model')

        pred = np.argmax(model.predict(img), axis=-1)
        pred = ENCODER.inverse[pred[0]]

        correct = 'yes' if pred == question else 'no'

        return render_template('practice.html', q=choice(list(ENCODER.keys())), correct=correct)

    except Exception as e:
        print(e)
        return render_template('error.html')


@app.route('/quiz', methods=['GET'])
def quiz_get():

    if 'progress' not in session:
        session['progress'] = QUIZ_PROG[:]

    progress = session['progress']

    # get a random character that hasn't been tested yet
    possible = [x[0] for x in progress if x[1] != '' and x[2] == 0]
    if possible:
        q = choice(possible)
    else:
        q = 'done'

    # split the progress array into rows
    # so that it's easier to render
    render_prog = []
    for i in range(0, 50, 10):
        render_prog.append(progress[i:i+10])

    return render_template('quiz.html', q=q, progress=render_prog)


@app.route('/quiz', methods=['POST'])
def quiz_post():

    try:
        # get data from the request
        question = request.form['question']
        pixels_str = request.form['pixels']
        pixels = pixels_str.split(',')
        img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)

        model = keras.models.load_model('kana.model')

        # make a prediction
        pred = np.argmax(model.predict(img), axis=-1)
        pred = ENCODER.inverse[pred[0]]

        # indicator for the `progress` array
        # 0 -> unanswered, 1 -> correct, 2 -> incorrect
        result = 1 if pred == question else 2

        # update the progress
        progress = session['progress']

        val = (question, CHAR_MAP.inverse[question], 0)
        upated_val = (question, CHAR_MAP.inverse[question], result)

        progress[progress.index(val)] = upated_val
        session['progress'] = progress

        return redirect(url_for('quiz_get'))

    except Exception as e:
        print(e)
        return render_template('error.html')


if __name__ == '__main__':
    # these are just settings for developing to allow
    # connection to the dev server from different devices,
    # a real webserver would be used for a legit deployment
    # app.run(host='0.0.0.0', port=8082, threaded=True)
    app.run()
