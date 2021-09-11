<?php

function returnResponse($res) {
    echo json_encode($res);
}

$IP = "192.168.1.179";
$PORT = 8080;

$_POST = json_decode(file_get_contents('php://input'), true); // decoding the posted JSON

header("Content-Type: application/json; charset=UTF-8");
$response = array();

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    http_response_code(500);

    $response["status"] = -1;
    $response["message"] = "Failed to create a socket connection: " . socket_strerror(socket_last_error());

    returnResponse($response);
    return;
}

$status = socket_connect($socket, $IP, $PORT);

if ($status === false) {
    http_response_code(503);

    $response["status"] = -2;
    $response["message"] = "Could not connect over local network.";

    returnResponse($response);
    return;
}

list($r, $g, $b) = sscanf($_POST["colourCode"], "#%02x%02x%02x");

if ($_POST["requestType"] == "static") {
    $in = sprintf("set r %d\n set g %d\n set b %d\nsave\n", $r, $g, $b);
}

else if ($_POST["requestType"] == "preset") {

    $allFiles = scandir("../light-scripts"); // Or any other directory
    $files = array_diff($allFiles, array('.', '..'));

    if (in_array($_POST["name"], $files)) {
        $in = file_get_contents("../light-scripts/" . $_POST["name"]);
    }

    else {
        http_response_code(500);
        $response["status"] = -69;
        $response["message"] = "Stop hacking :("
        return;
    }
    
}

$out = "";

echo "Sending HTTP HEAD request...";
socket_write($socket, $in, strlen($in));
echo "OK.\n";

echo "Reading response:\n\n";
while ($out = socket_read($socket, 2048)) {
    $response["message"] .= $out;
}

socket_close($socket);
http_response_code(200);
$response["status"] = 0;
returnResponse($response);
?>
