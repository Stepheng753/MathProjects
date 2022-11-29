let answerInput;
let randNum1 = 0;
let randNum2 = 0;
let points = 0;
let range1;
let range2;
let timeTotal = 60;
let timeLeft;
let numAnsWin = timeTotal / 2;
let numInput;
let startTimer;
let start = 0;
let stopped = 0;
let difficulty = 'Medium';
let timerDom = document.getElementById('time-counter');
let pointsDom = document.getElementById('points-counter');
let submitDom = document.getElementById('submitForm');
let canvasWidth = document.body.clientWidth;

function setup() {
	let cnv = createCanvas(750, 750);
	cnv.parent('sketchHolder');

	numInput = createInput('');
	numInput.position(canvasWidth * 0.31 + width / 4, height / 2, 'relative');
	numInput.size(width * 0.49);
	numInput.parent('sketchHolder');
	numInput.input(myInputEvent);

	setDifficulty(difficulty);
	reset();
}

function setDifficulty(diff) {
	difficulty = diff;
	if (difficulty == 'Easy') {
		range1 = 5;
		range2 = 5;
	} else if (difficulty == 'Medium') {
		range1 = 12;
		range2 = 12;
	} else {
		range1 = 15;
		range2 = 15;
	}
	startTimer = false;
	document.getElementById('difficultyChosen').innerHTML = difficulty;
	reset();
}

function myInputEvent() {
	if (!startTimer) {
		startTimer = true;
		start = millis();
	}
	answerInput = !isNaN(parseInt(this.value())) ? parseInt(this.value()) : 'Not Number';
}

function draw() {
	background(0);
	push();
	for (let i = 0; i < points; i++) {
		colorMode(HSB);
		var strokeCol = map((i / numAnsWin) * width, 0, width, 0, 360);
		fill(strokeCol, 100, 100);
		rect((i / numAnsWin) * width, 0, width / numAnsWin, height);
	}
	pop();

	if (timeLeft != 0 && points < numAnsWin) {
		if (startTimer) {
			timeLeft = (timeTotal - (millis() - start) / 1000).toFixed(2);
			if (timeLeft < 0) {
				timeLeft = 0;
			}
		}

		timerDom.innerHTML = 'Time Left: ' + Math.abs(timeLeft).toFixed(2) + ' secs';
		if (!startTimer && points == -1) {
			pointsDom.innerHTML = 'Points: 0';
		} else {
			pointsDom.innerHTML = 'Points: ' + points;
		}

		push();
		fill(0, 0, 0, 100);
		rect(width / 4, height / 4, width / 2, height / 2);
		strokeWeight(5);
		fill(255);
		textSize(45);
		text(randNum1 + ' × ' + randNum2, width * 0.42, height * 0.45);
		pop();

		if (answerInput == randNum1 * randNum2) {
			points++;
			randNum1 = floor(random(0, range1 + 1));
			randNum2 = floor(random(0, range2 + 1));
			numInput.value('');
			answerInput = null;
		}
	} else {
		numInput.hide();
		push();
		fill(0, 0, 0, 100);
		rect(width / 4, height / 3, width / 2, height / 3);
		strokeWeight(5);
		fill(255);
		textSize(20);
		text('Total Points: ' + points, width / 3.9, height / 3 + height / 16);
		if (points >= numAnsWin) {
			text('Winner Winner!', width / 3.9, height / 3 + height / 6);
			text('Time: ' + (timeTotal - timeLeft).toFixed(2) + ' secs', width / 3.9, (2 * height) / 3 - height / 16);
			createFormDom();
		} else if (points == 0) {
			text('No Points!', width / 3.9, height / 3 + height / 6);
		} else {
			text('Try Again!', width / 3.9, height / 3 + height / 6);
		}
		pop();
		noLoop();
	}
}

function reset() {
	loop();
	points = -1;
	randNum1 = 0;
	randNum2 = 0;
	numInput.show();
	timeLeft = timeTotal;
}

function createFormDom() {
	submitDom.innerHTML += '<label>Enter in Name for Leaderboard:</label>';
	submitDom.innerHTML += '<br>';
	submitDom.innerHTML += "<input type='text' name='name' />";
	submitDom.innerHTML += "<input type='hidden' name='difficulty' id='difficulty' value='" + difficulty + "'/>";
	submitDom.innerHTML += "<input type='hidden' name='points' id='points' value='" + points + "'/>";
	submitDom.innerHTML +=
		"<input type='hidden' name='timePerPt' id='timePerPt' value='" + (timeTotal / points).toFixed(2) + "'/>";
	submitDom.innerHTML += '<br><br>';
	submitDom.innerHTML += "<input type='submit' name='submit'/>";
	submitDom.style.paddingBottom = '25px';
}
