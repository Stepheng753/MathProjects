let spacer = 250 / 7;
let numbers = [0, 0, 0, 0, 0, 0];
let targetNumber = 0;
let largeNums = [25, 50, 75, 100];
let smallNums = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10];
let selectAmtLargeNums;
let amtLargeNums = Math.floor(Math.random() * 4);
let startTime;
let totalTime = 30;
let selectSolutions;

function setup() {
	createCanvas(1000, 500);

	selectAmtLargeNums = createSelect();
	selectAmtLargeNums.position(10, 95);
	selectAmtLargeNums.size(100);
	for (let i = 0; i <= 4; i++) selectAmtLargeNums.option(i);
	selectAmtLargeNums.changed(() => {
		amtLargeNums = selectAmtLargeNums.value();
	});
}

function draw() {
	background('#2877AB');
	selectAmtLargeNums.selected(amtLargeNums);
	drawBoxes();
	showNumbers();
	startButton();
	stats();
}

function drawBoxes() {
	rectMode(CORNER);
	stroke(255);
	strokeWeight(2);

	// Target Number Box
	fill('#4B2DD7');
	rect(275, 35, 450, 180);

	// Random Number Box
	fill('#2854AB');
	for (let i = 0; i < 6; i++) {
		rect((1 + i) * spacer + i * 125, 260, 125, 180);
	}
}

function showNumbers() {
	stroke(0);
	strokeWeight(2);
	textAlign(CENTER);
	fill(255);

	textSize(128);
	text(targetNumber, 500, 165);

	textSize(50);
	for (let i = 0; i < 6; i++) {
		text(numbers[i], (i + 1) * spacer + (i + 1 / 2) * 125, 360);
	}
}

function mouseWithinStart(centerX, centerY, radius) {
	return (mouseX - centerX) ** 2 + (mouseY - centerY) ** 2 < radius ** 2;
}

function startButton() {
	push();
	fill(0);
	circle(950, 35, 50);

	fill('#50C878');
	stroke(0);
	strokeWeight(1);
	triangle(970, 35, 937, 50, 937, 20);
	pop();

	if (mouseIsPressed && mouseWithinStart(950, 35, 25)) {
		let shuffleLargeIndex = shuffle([...Array(largeNums.length).keys()]);
		let shuffleSmallIndex = shuffle([...Array(smallNums.length).keys()]);
		for (let i = 0; i < 6; i++) {
			if (i < amtLargeNums) {
				numbers[i] = largeNums[shuffleLargeIndex[i]];
			} else {
				numbers[i] = smallNums[shuffleSmallIndex[i]];
			}
		}
		targetNumber = Math.floor(Math.random() * 899) + 100;
		startTime = millis();
	}

	stroke(0);
	strokeWeight(2);
	textAlign(LEFT);
	fill(255);
	textSize(16);
	text('Select Amount of Large Numbers:', 10, 20);
}

function stats() {
	let timeRemaining = parseFloat(totalTime - (millis() - startTime) / 1000).toFixed(2);
	if (!isNaN(timeRemaining) && timeRemaining > 0) {
		text('Time Remaining: ' + timeRemaining + ' secs', 10, 75);
	} else if (!isNaN(timeRemaining) && timeRemaining <= 0) {
		text('Time Remaining: 0.00 secs', 10, 75);
		let solutions = loops(numbers, targetNumber);

		selectSolutions = createSelect();
		selectSolutions.position(10, 155);
		selectSolutions.size(250);
		selectSolutions.option('See the following solutions:');
		if (solutions == 'No Solutions') {
			selectSolutions.option(solutions);
		} else {
			solutions.forEach((sol) => {
				selectSolutions.option(sol);
			});
		}
	}
}

function shuffle(arr) {
	for (let i = arr.length - 1; i > 0; i--) {
		let randIndex = Math.floor(Math.random() * (i + 1));
		let currentElement = arr[i];
		arr[i] = arr[randIndex];
		arr[randIndex] = currentElement;
	}
	return arr;
}
