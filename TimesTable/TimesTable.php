<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />

		<title>Times Table</title>

		<style type="text/css">
			body {
				width: 1000px;
				margin: auto;
				text-align: center;
			}
			a:hover {
				color: blue;
			}
			a:active {
				color: red;
			}
			a:visited {
				color: #000;
			}
			a {
				margin-left: 30px;
				margin-right: 30px;
				text-decoration: underline;
			}
			#sketchHolder {
				width: 1000px;
				height: 400px;
				margin: 0 auto;
				position: relative;
			}
			table, th, td {
                margin-left: auto;
                margin-right: auto;
                border: 1px solid black;
                table-layout: fixed ;
                width: 100% ;
            }
            #highlight-row {
                background-color: lightsalmon;
            }
		</style>

		<script src="https://cdn.jsdelivr.net/npm/p5@1.2.0/lib/p5.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.5.11/addons/p5.dom.min.js"></script>
	</head>

	<body>
		<h1 style="padding: 0">Times Table</h1>
		<a id="Easy" onclick="javascript:setDifficulty('Easy')">Easy</a>
		<a id="Medium" onclick="javascript:setDifficulty('Medium')">Medium</a>
		<a id="Hard" onclick="javascript:setDifficulty('Hard')">Hard</a>
		<div id="difficultyChosen" style="padding-top: 15px;"></div>
		<div style="padding-bottom: 25px; padding-top: 15px">
			<div id="points-counter" style="display: inline-block; padding-right: 15px"></div>
			<div id="time-counter" style="display: inline-block; padding-left: 15px"></div>
		</div>

		<form action="./TimesTable.php" id="submitForm" method="POST""></form>
		<?php 
        require_once('../../../PHPConnect/connectStore.php');
        if (isset($_POST) && array_key_exists('submit', $_POST)) {
            $dbc = @mysqli_connect(DB_HOST, LB_DB_USER, LB_DB_PASSWORD, LB_DB_NAME, DB_PORT)
            OR die('Could not connect to MySQL: ' . mysqli_connect_error());

            $name = $_POST['name'];
            $difficulty = $_POST['difficulty'];
            $points = $_POST['points'];
			$timePerPt = $_POST['timePerPt'];

            $sql = '';
            if (isset($name) && !empty($name)) {
				$sql = "INSERT INTO `timesTableLB`(`name`, `difficulty`, `points`, `timePerPt`) VALUES ('". $name . "','" . $difficulty . "','" . $points . "','" . $timePerPt . "')";
                if ($dbc->query($sql) === TRUE) {
					echo "New record created successfully";
				} else {
					echo "Error: " . $sql . "<br>" . $dbc->error;
				}
            } else {
                echo "No Name Given";
            }
            echo "<br><br>";
            $query = "SELECT * FROM `timesTableLB` WHERE difficulty='" . $difficulty ."' ORDER BY `timePerPt`";
            $response = @mysqli_query($dbc, $query);
            $count = 1;
            if($response){
                echo "<table style='align'>";
                echo "<tr>";
                echo "<th>Rank</th>";
                echo "<th>Name</th>";
                echo "<th>Points</th>";
				echo "<th>Seconds Per Point</th>";
                echo "</tr>";
                while($row = mysqli_fetch_array($response)){
                    if ($row['name'] == $name && $row['points'] == $points && $row['timePerPt'] == $timePerPt) {
                        echo "<tr id='highlight-row'>";
                    } else {
                        echo "<tr>";
                    }
                    echo "<td>" . $count++ . "</td>";
                    echo "<td>" . $row['name'] . "</td>";
                    echo "<td>" . $row['points'] . "</td>";
					echo "<td>" . $row['timePerPt'] . "</td>";
                    echo "</tr>";
                }
                echo "</table>";
            }
            echo " <div style='padding-bottom: 25px;'></div>";
		}
		?>

		<div id="sketchHolder"></div>
		<script src="TimesTable.js"></script>
		<script>
        if ( window.history.replaceState ) {
            window.history.replaceState( null, null, window.location.href );
        }
    </script>
	</body>
</html>
