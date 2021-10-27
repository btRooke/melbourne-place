<?php

function returnResponse($res) {
    echo json_encode($res);
}

$DOORBELL_IP = "192.168.1.194"; // most certainly a security risk
$DOORBELL_PORT = 42069;

$_POST = json_decode(file_get_contents('php://input'), true); // decoding the posted JSON

header("Content-Type: application/json; charset=UTF-8");
$response = array();

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

if ($socket === false) {

    http_response_code(500);

    $response["status"] = -1;
    $response["message"] = "Failed to create a socket connection: " . socket_strerror(socket_last_error()) . ".";

    returnResponse($response);

    return;
}

$status = socket_connect($socket, $DOORBELL_IP, $DOORBELL_PORT);

if ($status === false) {

    http_response_code(503);

    $response["status"] = -2;
    $response["message"] = "Could not connect connect to doorbell over local network.";

    returnResponse($response);
    
    return;
}

if (array_key_exists("morseMessage", $_POST)) {
    socket_write($socket, $_POST["morseMessage"], strlen($_POST["morseMessage"]));
}

$out = "";

echo "Reading response:\n\n";
while ($out = socket_read($socket, 2048)) {
    $response["message"] .= $out;
}

socket_close($socket);

http_response_code(200);

$response["status"] = 0;

returnResponse($response);

?>
