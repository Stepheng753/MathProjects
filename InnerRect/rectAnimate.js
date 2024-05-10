let R;
let n;
let m;
let currX = 0;
let currY = 0;
let currW = 0;
let currH = 0;
let currDimN = 1;
let currDimM = 1;
let count = 0;
let findSquare = true;

function setup() {
	frameRate(2);
	let cnvs = createCanvas(750, 500);
	cnvs.parent('canvas-parent');
	R = new Rectangle(0, 0, 750, 500);

	n = parseInt(document.getElementById('n').value);
	m = parseInt(document.getElementById('m').value);
}

function draw() {
	background(255);
	R.drawInnerSquares();

	drawNbyMRect(R, currDimN, currDimM);
	document.getElementById('counter').innerHTML = ++count;

	if (currW == 0 && currH == 0 && !findSquare) {
		currDimM++;
		if (currDimM > m) {
			currDimM = 1;
			currDimN++;
			if (currDimN > n) {
				currDimN = 1;
				currDimM = 1;
				count = 0;
				findSquare = true;
				return;
			}
		}
	}
	if (currW == 0 && currH == 0 && findSquare) {
		console.log(currDimN, currDimM);
		currDimM++;
		currDimN++;
		if (currDimM > m || currDimN > n) {
			currDimN = 1;
			currDimM = 1;
			count = 0;
			findSquare = false;
		}
	}
}

function drawNbyMRect(R, dimN, dimM) {
	currW = (dimM * R.w) / m;
	currH = (dimN * R.h) / n;
	R.highlightRect(currX, currY, currW, currH);
	currX += R.w / m;
	if (currX >= (R.w * (m + 1 - dimM)) / m) {
		currX = 0;
		currY += R.h / n;
		if (currY >= (R.h * (n + 1 - dimN)) / n) {
			currX = 0;
			currY = 0;
			currW = 0;
			currH = 0;
		}
	}
}

class Rectangle {
	constructor(x, y, w, h) {
		this.x = x;
		this.y = y;
		this.w = w;
		this.h = h;
	}

	drawInnerSquares() {
		for (let row = 0; row < this.h; row += this.h / n) {
			for (let col = 0; col < this.w; col += this.w / m) {
				strokeWeight(3);
				rect(col, row, this.w / m, this.h / n);
			}
		}
	}

	highlightRect(x, y, w, h) {
		if (findSquare) {
			stroke(200, 0, 0);
			fill(180, 69, 69);
		} else {
			stroke(0, 200, 0);
			fill(80, 170, 110);
		}
		rect(x, y, w, h);
		stroke(0);
		fill(255);
	}
}
