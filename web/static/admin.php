<!DOCTYPE html>
<html lang="en-gb">

    <head>

        <title>Melbourne Place</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="core.css">
        <link rel="stylesheet" href="admin.css">

        <!-- for fonts -->

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Open+Sans&display=swap" rel="stylesheet">

        <!-- for bell animations -->

        <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.4/lottie.min.js"></script>

        <!-- for progressive web apps -->

        <link rel="manifest" href="manifest.json">

    </head>

    <body>

        <div class="fullScreen centreContent noselect">

        <?php

        $DB_HOSTNAME = "localhost";
        $DB_USER     = "melbournePlace";
        $DB_PASS     = "J1#23h7c$?.##{<#";
        $DB_NAME     = "melbournePlace";

        if ($_POST["key"] === "cooladmin123") {

            echo "<h1>welcom to the admin page :)))</h1>";            

        }

        else {

            echo "<form action=\"\" method=\"post\">";
            echo "<div>";
            echo "<label>Enter Password: </label>";
            echo "<input type=\"text\" name=\"key\" id=\"key\" required>";
            echo "</div>";
            echo "</form>";

        }

        ?>

        </div>

    </body>

</html>
