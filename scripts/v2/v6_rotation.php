
<!DOCTYPE html>
<html lang="en">
<head>
  <title>VRO</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>


<div class="container">
  <h2>Volleyball Rotation Optimizer (VRO)</h2>
<br>
	<h3>This is an application that provides coaches and captains a mathematical way of deciding where all players should start on a court based on their skill levels</h3>
		<br>	
	<h4>By entering in each player's name, front row skill level and back row skill level, VRO will generate the most balanced rotation for you. </h4>  
		<br>
<p>Skills are ranked 5 being the best, 1 being the worst.</p>
<form method="post" action="v6_rotation.php">

<div class="dropdown">
  <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Rotation Selection
  <span class="caret"></span></button>
  <ul class="dropdown-menu">
    <li><a href="#">6-2</a></li>

  </ul>
</div>

<br>
<div class="form-group row">
<div class="col-xs-3">


	<b><p>Name</p></b>

    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>
    <input class="form-control" id="ex3" type="text" name="p1_name" tabindex = 1 required>
	</div>

	<br>

    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>

    <input class="form-control" id="ex3" type="text" name="p2_name" tabindex = 4 required>
	</div>
		<br>

    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>
    <input class="form-control" id="ex3" type="text" name="p3_name" tabindex = 7 required>
	</div>
		<br>

    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>
    <input class="form-control" id="ex3" type="text" name="p4_name" tabindex = 10 required>
	</div>
		<br>
    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>

    <input class="form-control" id="ex3" type="text" name="p5_name" tabindex = 13 required>
	</div>
		<br>
    <div class="input-group">
      <span class="input-group-addon">
        <input type="radio" aria-label="Checkbox for following text input">
      </span>
    <input class="form-control" id="ex3" type="text" name="p6_name" tabindex = 16 required>
	</div>
		<br>
</div>

<div class="col-xs-2">
	<b><p>Front Row Skill (1-5)</p></b>
    <input class="form-control" id="ex1" type="text" name="p1_FR" tabindex = 2 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p2_FR" tabindex = 5 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p3_FR" tabindex = 8 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p4_FR" tabindex = 11 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p5_FR" tabindex = 14 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p6_FR" tabindex = 17 required>
	<br>
</div>

<div class="col-xs-2">
	<b><p>Back Row Skill (1-5)</p></b>
    <input class="form-control" id="ex1" type="text" name="p1_BR" tabindex = 3 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p2_BR" tabindex = 6 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p3_BR" tabindex = 9 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p4_BR" tabindex = 12 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p5_BR" tabindex = 15 required>
	<br>
    <input class="form-control" id="ex3" type="text" name="p6_BR" tabindex = 18 required>
	<br>
</div>


</div>
    <input type="submit" value="Optimize!!" name="submit"> <!-- assign a name for the button -->
</form>



<?php 

function display()
{


$p1_name = $_POST["p1_name"];
$p2_name = $_POST["p2_name"];
$p3_name = $_POST["p3_name"];
$p4_name = $_POST["p4_name"];
$p5_name = $_POST["p5_name"];
$p6_name = $_POST["p6_name"];

$p1_FR = $_POST["p1_FR"];
$p2_FR = $_POST["p2_FR"];
$p3_FR = $_POST["p3_FR"];
$p4_FR = $_POST["p4_FR"];
$p5_FR = $_POST["p5_FR"];
$p6_FR = $_POST["p6_FR"];


$p1_BR = $_POST["p1_BR"];
$p2_BR = $_POST["p2_BR"];
$p3_BR = $_POST["p3_BR"];
$p4_BR = $_POST["p4_BR"];
$p5_BR = $_POST["p5_BR"];
$p6_BR = $_POST["p6_BR"];

$command = escapeshellcmd('/var/www/html/VRO/rotation.py ');

//$arr = array('p1' => $p1_name, array();


$arr = array('p1' => array($p1_name, $p1_FR, $p1_BR), 'p2' => array($p2_name, $p2_FR, $p2_BR), 'p3' => array($p3_name, $p3_FR, $p3_BR), 'p4' => array($p4_name, $p4_FR, $p4_BR), 'p5' => array($p5_name, $p5_FR, $p5_BR), 'p6' => array($p6_name, $p6_FR, $p6_BR));

$result = shell_exec('python /var/www/html/VRO/json_testing/jsonpy2.py ' . escapeshellarg(json_encode($arr)));

echo $result;


}

{
   display();
} 
?>

		</div>
	</div>
</div>
<br>
<p>---------------------------</p>

<h5>Things that still need to be added</h5>
<p> - Rotation selection (5-1/6-2 etc) </p>
<p> - Lock in setter(s) </p>
<p> - Optimization isn't as optimal as it can be </p>
<p> - Try using 1/0 to decide if player should be FR or BR </p>
<p> - Everyone's potential setting skill level</p>
</body>
</html>