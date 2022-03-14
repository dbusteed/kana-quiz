// thanks to
// - http://www.williammalone.com/articles/create-html5-canvas-javascript-drawing-app/
// - https://stackoverflow.com/questions/17656292/html5-canvas-support-in-mobile-phone-browser

let context
let paint
let clickX = []
let clickY = []
let clickDrag = []

function startCanvas() {
  canvas = document.getElementById('canvas')
  context = canvas.getContext("2d")

  canvas.addEventListener("touchstart", function (e) {
    let touch = e.touches[0]
    let mouseEvent = new MouseEvent("mousedown", {
      clientX: touch.clientX,
      clientY: touch.clientY
    })
    canvas.dispatchEvent(mouseEvent)
  }, false)

  canvas.addEventListener("touchmove", function (e) {
    let touch = e.touches[0]
    let mouseEvent = new MouseEvent("mousemove", {
      clientX: touch.clientX,
      clientY: touch.clientY
    })
    canvas.dispatchEvent(mouseEvent)
  }, false)

  canvas.addEventListener("touchend", function (e) {
    let mouseEvent = new MouseEvent("mouseup")
    canvas.dispatchEvent(mouseEvent)
  }, false)

  $('#canvas').mousedown(function (e) {
    paint = true
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTope, false)
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
  context.clearRect(0, 0, 200, 200)
}

function resetCanvas() {
  clickX = []
  clickY = []
  clickDrag = []
  clearCanvas()
}

function redraw() {
  clearCanvas()

  for (let i = 0; i < clickX.length; i++) {
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
  let _pixels = []
  let pixels = []

  // rawPixels is [0, 0, 0, 0, ...], where a group of four
  // digits represent one pixel. so we're just grab every
  // fourth digit
  for (i = 0; i < rawPixels.length; i += 4) {
    _pixels.push(rawPixels[i + 3])
  }
    
  // compress image from 200x200 to 50x50
  for (i = 0; i < _pixels.length; i += 800) {
      for (j = 0; j < 200; j += 4) {
      pixels.push(_pixels[i+j])
    }
  }

  return pixels
}