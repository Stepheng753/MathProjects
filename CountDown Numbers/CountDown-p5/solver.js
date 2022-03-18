function combineArrs(arr1, arr2) {
	let arr1Index = 0;
	let arr2Index = 0;
	let combined = [];
	while (arr1Index < arr1.length && arr2Index < arr2.length) {
		combined.push(arr1[arr1Index++]);
		combined.push(arr2[arr2Index++]);
	}
	while (arr1Index < arr1.length) {
		combined.push(arr1[arr1Index++]);
	}
	while (arr2Index < arr2.length) {
		combined.push(arr2[arr2Index++]);
	}
	return combined;
}

function arithmetic(arr) {
	let answer = arr[0];
	for (let i = 1; i < arr.length; i += 2) {
		if (!Number.isInteger(answer) || answer < 0) return null;
		if (arr[i] == '+') answer += arr[i + 1];
		if (arr[i] == '-') answer -= arr[i + 1];
		if (arr[i] == '*') answer *= arr[i + 1];
		if (arr[i] == '/') answer /= arr[i + 1];
	}
	return answer;
}

function loops(numbers, targetNumber) {
	let operations = ['+', '-', '*', '/'];
	let solutionsArr = [];

	for (let i = 0; i < 6; i++) {
		let allNumbersPerm = removeDuplicates(permutations(numbers, i));
		let allOrderOperations = removeDuplicates(product(operations, i - 1));

		allNumbersPerm.forEach((numSeq) => {
			allOrderOperations.forEach((opSeq) => {
				let arr = combineArrs(numSeq, opSeq);
				let result = arithmetic(arr);
				if (result == targetNumber) {
					let arrStr = arr[0].toString();
					for (let i = 1; i < arr.length; i++) arrStr += ' ' + arr[i].toString();
					arrStr += ' = ' + targetNumber.toString();
					solutionsArr.push(arrStr);
				}
			});
		});
	}

	if (solutionsArr.length <= 0) {
		return 'No Solutions';
	}

	return solutionsArr;
}

function removeDuplicates(arr) {
	let noDuplicates = [];
	arr.forEach((element) => {
		if (!arrayIncludes(noDuplicates, element)) noDuplicates.push(element);
	});
	return noDuplicates;
}

function arrayIncludes(arr, element) {
	let returnVal = false;
	arr.forEach((item) => {
		if (JSON.stringify(element) == JSON.stringify(item)) returnVal = true;
	});
	return returnVal;
}
