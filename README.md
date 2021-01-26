# kana quiz

a machine learning web app that helps users practice writing Hiragana characters (one of the character sets used in the Japanese language)

---

## demo

### 1) practice mode
<img alt="demo of practice mode" src="./demo/practice.gif" height="400" width="400">

### 2) quiz mode
<img alt="demo of quiz mode" src="./demo/quiz.gif" height="500" width="400">

### 3) training mode
<img alt="demo of train mode" src="./demo/train.gif" height="400" width="400">

---

## run on your machine

### 1) environment setup
* clone the repo
* create and start a virtual environment (optional)
* install the following modules:
    * tensorflow
    * numpy (might come with tensorflow)
    * bidict
    * flask
    * flask_cors
    * matplotlib

### 2) app setup
* build the CNN model:
    ```
    python scripts/build_model.py
    ```
* run the app:
    ```
    python app.py
    ```
* go to [localhost:5000](http://localhost:5000)

### 3) useful scripts
* `scripts/model_development.ipynb`
    * notebook for developing / tuning the CNN model
* `scripts/data_distribution.py`
    * shows the distribution of instances within the dataset
    * ideally, this should be uniform across the 46 characters

---

## other notes

* the ML model / quiz only uses the basic Hiragana characters. I didn't wanna mess with diacritics (Gs, Zs, Ds, Bs, and Ps)
* i'm the only one who trained this model (so far), so it might be hypersensitive to my handwriting