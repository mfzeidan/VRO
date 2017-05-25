
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
  <h2>Volleyball Rotation Optimizer</h2>
  <p>Skills are ranked 5 being the best, 1 being the worst.</p>
<form method="post" action="v1_rotation.php">
<div class="form-group row">
<div class="col-xs-3">
	<b><p>Name</p></b>
    <input class="form-control" id="ex3" type="text" name="p1_name">
	<br>
    <input class="form-control" id="ex3" type="text" name="p2_name">
	<br>
    <input class="form-control" id="ex3" type="text" name="p3_name">
	<br>
    <input class="form-control" id="ex3" type="text" name="p4_name">
	<br>
    <input class="form-control" id="ex3" type="text" name="p5_name">
	<br>
    <input class="form-control" id="ex3" type="text" name="p6_name">
	<br>
</div>

<div class="col-xs-2">
	<b><p>Front Row Skill (1-5)</p></b>
    <input class="form-control" id="ex1" type="text" name="p1_FR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p2_FR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p3_FR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p4_FR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p5_FR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p6_FR">
	<br>
</div>

<div class="col-xs-2">
	<b><p>Back Row Skill (1-5)</p></b>
    <input class="form-control" id="ex1" type="text" name="p1_BR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p2_BR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p3_BR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p4_BR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p5_BR">
	<br>
    <input class="form-control" id="ex3" type="text" name="p6_BR">
	<br>
</div>


</div>
    <input type="submit" value="click" name="submit"> <!-- assign a name for the button -->
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

</body>
</html>