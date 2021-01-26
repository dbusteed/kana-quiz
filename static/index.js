var context
var paint
var clickX = new Array()
var clickY = new Array()
var clickDrag = new Array()

// adapted from http://www.williammalone.com/articles/create-html5-canvas-javascript-drawing-app/
// for mobile / touch https://stackoverflow.com/questions/17656292/html5-canvas-support-in-mobile-phone-browser

function startCanvas() {

    canvas = document.getElementById('canvas')
    context = canvas.getContext("2d")

    canvas.addEventListener("touchstart", function (e) {
        var touch = e.touches[0]
        var mouseEvent = new MouseEvent("mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY
        })
        canvas.dispatchEvent(mouseEvent)
    }, false)

    canvas.addEventListener("touchmove", function (e) {
        var touch = e.touches[0]
        var mouseEvent = new MouseEvent("mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY
        })
        canvas.dispatchEvent(mouseEvent)
    }, false)

    canvas.addEventListener("touchend", function (e) {
        var mouseEvent = new MouseEvent("mouseup")
        canvas.dispatchEvent(mouseEvent)
    }, false)

    $('#canvas').mousedown(function (e) {
        let mouseX = e.pageX - this.offsetLeft
        let mouseY = e.pageY - this.offsetTop
        paint = true
        addClick(mouseX, mouseY, false)
        redraw()
    })

    $('#canvas').mousemove(function (e) {
        if (paint) {
            addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true)
            redraw()
        }
    })

    $('#canvas').mouseup(function (e) {
        paint = false
        redraw()
    })

    $('#canvas').mouseleave(function (e) {
        paint = false
    })
}

function addClick(x, y, dragging) {
    clickX.push(x)
    clickY.push(y)
    clickDrag.push(dragging)
}

function clearCanvas() {
    context.clearRect(0, 0, 500, 500)
}

function resetCanvas() {
    clickX = new Array()
    clickY = new Array()
    clickDrag = new Array()
    clearCanvas()
}

function redraw() {
    clearCanvas()

    context.strokeStyle = "#000000"
    context.lineJoin = "round"
    context.lineWidth = 8

    for (var i = 0; i < clickX.length; i++) {
        context.beginPath()
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1])
        } else {
            context.moveTo(clickX[i] - 1, clickY[i])
        }
        context.lineTo(clickX[i], clickY[i])
        context.closePath()
        context.stroke()
    }
}

function sendTrainingData() {
    pixels = getPixels()
    document.getElementById('pixels').value = pixels
    document.getElementById('train-form').submit()
}

function sendQuizData() {
    pixels = getPixels()
    document.getElementById('pixels').value = pixels
    document.getElementById('quiz-form').submit()
}

function sendPracticeData() {
    pixels = getPixels()
    document.getElementById('pixels').value = pixels
    document.getElementById('practice-form').submit()
}

function getPixels() {
    let rawPixels = context.getImageData(0, 0, 200, 200).data
    let pixels = []

    // smush it
    for (i = 0; i < rawPixels.length; i += 16) {
        pixels.push(255 - rawPixels[i + 3])
    }

    return pixels
}