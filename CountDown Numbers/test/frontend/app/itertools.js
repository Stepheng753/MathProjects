// Taken from Justin Fay
// https://gist.github.com/justinfay/f30d53f8b85a274aee57

export function permutations(array, r) {
	// Algorythm copied from Python `itertools.permutations`.
	var n = array.length;
	if (r === undefined) {
		r = n;
	}
	if (r > n) {
		return;
	}
	var indices = [];
	for (var i = 0; i < n; i++) {
		indices.push(i);
	}
	var cycles = [];
	for (var i = n; i > n - r; i--) {
		cycles.push(i);
	}
	var results = [];
	var res = [];
	for (var k = 0; k < r; k++) {
		res.push(array[indices[k]]);
	}
	results.push(res);

	var broken = false;
	while (n > 0) {
		for (var i = r - 1; i >= 0; i--) {
			cycles[i]--;
			if (cycles[i] === 0) {
				indices = indices.slice(0, i).concat(indices.slice(i + 1).concat(indices.slice(i, i + 1)));
				cycles[i] = n - i;
				broken = false;
			} else {
				var j = cycles[i];
				var x = indices[i];
				indices[i] = indices[n - j];
				indices[n - j] = x;
				var res = [];
				for (var k = 0; k < r; k++) {
					res.push(array[indices[k]]);
				}
				results.push(res);
				broken = true;
				break;
			}
		}
		if (broken === false) {
			break;
		}
	}
	return results;
}

// Taken from Ryan Kane
// https://gist.github.com/cybercase/db7dde901d7070c98c48#gistcomment-2400061

export function product(iterables, repeat) {
	var argv = Array.prototype.slice.call(arguments),
		argc = argv.length;
	if (argc === 2 && !isNaN(argv[argc - 1])) {
		var copies = [];
		for (var i = 0; i < argv[argc - 1]; i++) {
			copies.push(argv[0].slice()); // Clone
		}
		argv = copies;
	}
	return argv.reduce(
		function tl(accumulator, value) {
			var tmp = [];
			accumulator.forEach(function (a0) {
				value.forEach(function (a1) {
					tmp.push(a0.concat(a1));
				});
			});
			return tmp;
		},
		[[]]
	);
}
