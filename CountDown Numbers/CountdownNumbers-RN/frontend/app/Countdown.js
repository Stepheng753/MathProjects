import { StatusBar } from 'expo-status-bar';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { Audio } from 'expo-av';
import { arithmetic, loops } from './solver';

const screenHeight = Math.round(Dimensions.get('window').height);
const screenWidth = Math.round(Dimensions.get('window').width);
let largeNums = [25, 50, 75, 100];
let smallNums = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10];
let totalTime = 30;

const wait = (timeout) => {
	return new Promise((resolve) => setTimeout(resolve, timeout));
};

function Countdown(props) {
	const [randNums, setRandNums] = useState([0, 0, 0, 0, 0, 0]);
	const [targetNum, setTargetNum] = useState(0);
	const [amtLargeNums, setAmtLargeNums] = useState(Math.floor(Math.random() * 4));
	const [timeRemaining, setTimeRemaining] = useState(0);
	const [timerIsRunning, setTimerIsRunning] = useState(false);
	const [solutions, setSolutions] = useState([]);
	const [attemptedAnswer, setAttemptedAnswer] = useState([]);
	const [attemptedAnswerStr, setAttemptedAnswerStr] = useState('');
	const [pressedHistory, setPressedHistory] = useState([]);
	const [answerCorrect, setAnswerCorrect] = useState(false);
	const [sound, setSound] = React.useState();

	const start = async () => {
		if (timerIsRunning) {
			setTimerIsRunning(false);
			setRandNums([0, 0, 0, 0, 0, 0]);
			setTargetNum(0);
			setTimeRemaining(0);
			await sound.pauseAsync();
			await sound.setPositionAsync(0);
		}
		if (!timerIsRunning) {
			const { sound } = await Audio.Sound.createAsync(require('../assets/CountdownAudio.mp3'));
			setSound(sound);
			setSolutions([]);
			randomizeNumbers();
			setTimerIsRunning(true);
			setTimeRemaining(totalTime);
			appendAnswer('C');
			setAnswerCorrect(false);
			await sound.playAsync();
		}
	};

	useEffect(() => {
		if (answerCorrect) {
			setTimerIsRunning(false);
			if (targetNum != 0) setSolutions(loops(randNums, targetNum));
		}
		if (timeRemaining <= 1) {
			setTimerIsRunning(false);
			if (targetNum != 0) setSolutions(loops(randNums, targetNum));
		}
		if (timerIsRunning) {
			wait(1000).then(() => {
				setTimeRemaining(timeRemaining - 1);
			});
		}
		if (!timerIsRunning) {
			setTimeRemaining(0);
		}
	}, [timeRemaining]);

	const randomizeNumbers = () => {
		let shuffleLargeIndex = shuffle([...Array(largeNums.length).keys()]);
		let shuffleSmallIndex = shuffle([...Array(smallNums.length).keys()]);
		let numbers = randNums;
		for (let i = 0; i < randNums.length; i++) {
			if (i < amtLargeNums) {
				numbers[i] = largeNums[shuffleLargeIndex[i]];
			} else {
				numbers[i] = smallNums[shuffleSmallIndex[i]];
			}
		}
		setRandNums(numbers);
		setTargetNum(Math.floor(Math.random() * 899) + 100);
	};

	const createSolutionPicker = () => {
		let pickerItems = [<Picker.Item label={'See the following solutions'} key={-1} />];
		if (solutions == 'No Solutions') {
			pickerItems.push(<Picker.Item label="No Solutions" value={0} key={1} />);
		} else {
			for (let i = 0; i < solutions.length; i++) {
				pickerItems.push(<Picker.Item label={solutions[i]} value={0} key={i} />);
			}
		}
		return <Picker style={[styles.picker, { top: '.5%' }]}>{pickerItems}</Picker>;
	};

	const createNumberBoxes = () => {
		let numberBoxes1 = [];
		let numberBoxes2 = [];
		for (let i = 0; i < 6; i++) {
			if (i < 3) {
				numberBoxes1.push(
					<TouchableOpacity
						style={[
							styles.numberBox,
							pressedHistory.includes(i)
								? { backgroundColor: '#e74856' }
								: { backgroundColor: '#2854AB' },
						]}
						onPress={() => appendAnswer(randNums[i], i)}
						key={i}
					>
						<Text style={styles.randomNumber}>{randNums[i]}</Text>
					</TouchableOpacity>
				);
			} else {
				numberBoxes2.push(
					<TouchableOpacity
						style={[
							styles.numberBox,
							pressedHistory.includes(i)
								? { backgroundColor: '#e74856' }
								: { backgroundColor: '#2854AB' },
						]}
						onPress={() => appendAnswer(randNums[i], i)}
						key={i}
					>
						<Text style={styles.randomNumber}>{randNums[i]}</Text>
					</TouchableOpacity>
				);
			}
		}
		return (
			<View>
				<View style={styles.numberRow}>{numberBoxes1}</View>
				<View style={styles.numberRow}>{numberBoxes2}</View>
			</View>
		);
	};

	const appendAnswer = (itemToAppend, numIndex) => {
		let arrayLength = attemptedAnswer.length;
		if (itemToAppend == 'C') {
			setAttemptedAnswerStr('');
			setAttemptedAnswer([]);
			setPressedHistory([]);
			setAnswerCorrect(false);
		} else if (arrayLength != 11 && !answerCorrect) {
			if (
				(arrayLength == 0 && Number.isInteger(itemToAppend)) ||
				(Number.isInteger(attemptedAnswer[arrayLength - 1]) &&
					!Number.isInteger(itemToAppend) &&
					!attemptedAnswerStr.includes('NaN')) ||
				(!Number.isInteger(attemptedAnswer[arrayLength - 1]) &&
					Number.isInteger(itemToAppend) &&
					!pressedHistory.includes(numIndex))
			) {
				setAttemptedAnswerStr(showAnswers([...attemptedAnswer, itemToAppend]));
				setAttemptedAnswer([...attemptedAnswer, itemToAppend]);
				setPressedHistory([...pressedHistory, numIndex]);
			}
		}
	};

	const showAnswers = (arr) => {
		let result;
		if (!Number.isInteger(arr[arr.length - 1]) || arithmetic(arr) == null) result = 'NaN';
		else result = arithmetic(arr);
		let arrStr = arr[0].toString();
		for (let i = 1; i < arr.length; i++) {
			arrStr += ' ' + arr[i].toString();
		}
		arrStr += ' = ' + result.toString();

		if (targetNum == result && timerIsRunning) {
			setAnswerCorrect(true);
		}
		return arrStr;
	};

	return (
		<View style={styles.container}>
			<View
				style={[
					styles.targetBox,
					answerCorrect ? { backgroundColor: '#50C878' } : { backgroundColor: '#4B2DD7' },
				]}
			>
				<Text style={styles.targetNumber}>{targetNum}</Text>
			</View>
			<Picker
				selectedValue={amtLargeNums}
				onValueChange={(itemValue) => setAmtLargeNums(itemValue)}
				style={styles.picker}
			>
				<Picker.Item label="0 Large Numbers, 6 Small Numbers" value={0} />
				<Picker.Item label="1 Large Numbers, 5 Small Numbers" value={1} />
				<Picker.Item label="2 Large Numbers, 4 Small Numbers" value={2} />
				<Picker.Item label="3 Large Numbers, 3 Small Numbers" value={3} />
				<Picker.Item label="4 Large Numbers, 2 Small Numbers" value={4} />
			</Picker>
			<View style={styles.centerArea}>
				<TouchableOpacity style={styles.startButton} onPress={() => start()}>
					<View style={styles.circle} />
					<View style={styles.triangle} />
				</TouchableOpacity>
				<View style={styles.timer}>
					<Text style={styles.timeRemaining}>Time Remaining:</Text>
					<Text style={styles.counter}>{timeRemaining} secs</Text>
				</View>
			</View>
			{createSolutionPicker()}
			<View style={styles.mathShower}>
				<Text style={styles.attemptedAnswer}>{attemptedAnswerStr}</Text>
			</View>
			<View style={styles.numberRow}>
				<TouchableOpacity style={[styles.numberBox, styles.operations]} onPress={() => appendAnswer('+')}>
					<Text style={styles.randomNumber}>{'+'}</Text>
				</TouchableOpacity>
				<TouchableOpacity style={[styles.numberBox, styles.operations]} onPress={() => appendAnswer('-')}>
					<Text style={styles.randomNumber}>{'-'}</Text>
				</TouchableOpacity>
				<TouchableOpacity style={[styles.numberBox, styles.operations]} onPress={() => appendAnswer('*')}>
					<Text style={[styles.randomNumber, { fontSize: 55 }]}>{'\u2715'}</Text>
				</TouchableOpacity>
				<TouchableOpacity style={[styles.numberBox, styles.operations]} onPress={() => appendAnswer('/')}>
					<Text style={styles.randomNumber}>{'\u00F7'}</Text>
				</TouchableOpacity>
				<TouchableOpacity style={[styles.numberBox, styles.operations]} onPress={() => appendAnswer('C')}>
					<Text style={styles.randomNumber}>{'C'}</Text>
				</TouchableOpacity>
			</View>
			{createNumberBoxes()}

			<StatusBar style="auto" />
		</View>
	);
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

export default Countdown;

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: '#2877AB',
		alignItems: 'center',
		justifyContent: 'center',
	},
	targetBox: {
		height: screenHeight * 0.18,
		width: screenWidth * 0.84,
		borderWidth: 4,
		borderColor: '#fff',
		alignItems: 'center',
	},
	numberBox: {
		height: screenHeight * 0.16,
		width: screenWidth * 0.28,
		margin: 10,
		borderWidth: 4,
		borderColor: '#fff',
		alignItems: 'center',
		justifyContent: 'center',
	},
	numberRow: {
		flexDirection: 'row',
		top: '7%',
	},
	triangle: {
		borderStyle: 'solid',
		borderTopWidth: 25,
		borderRightWidth: 0,
		borderBottomWidth: 25,
		borderLeftWidth: 45,
		borderTopColor: 'transparent',
		borderBottomColor: 'transparent',
		borderLeftColor: '#50C878',
		alignSelf: 'center',
		bottom: '50%',
		left: '8%',
	},
	circle: {
		padding: 40,
		borderRadius: 50,
		backgroundColor: '#555',
	},
	startButton: {
		top: '10%',
		right: '15%',
	},
	timer: {
		top: '3%',
		left: '40%',
	},
	timeRemaining: {
		color: '#fff',
		fontSize: 20,
	},
	centerArea: {
		flexDirection: 'row',
		alignItems: 'center',
		justifyContent: 'center',
		width: '80%',
	},
	randomNumber: {
		fontWeight: 'bold',
		color: '#fff',
		fontSize: 75,
	},
	targetNumber: {
		fontWeight: 'bold',
		color: '#fff',
		fontSize: 150,
	},
	counter: {
		color: '#fff',
		fontSize: 30,
		textAlign: 'center',
	},
	picker: {
		width: screenWidth * 0.8,
		height: 20,
		color: '#fff',
		top: '2%',
	},
	attemptedAnswer: {
		color: '#fff',
		fontWeight: 'bold',
		fontSize: 40,
		borderWidth: 2,
		padding: 10,
		borderTopColor: 'transparent',
		borderRightColor: 'transparent',
		borderLeftColor: 'transparent',
		borderBottomColor: '#fff',
		top: '30%',
		width: screenWidth * 0.85,
	},
	operations: {
		height: screenHeight * 0.1,
		width: screenWidth * 0.15,
		backgroundColor: '#2854AB',
	},
});
