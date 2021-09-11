<!DOCTYPE html>
<html lang="en-gb">

    <head>

        <title>Melbourne Place</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="core.css">

        <!-- for fonts -->

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Open+Sans&display=swap" rel="stylesheet">

        <!-- for bell animations -->

        <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.4/lottie.min.js"></script>

        <!-- for progressive web apps -->

        <link rel="manifest" href="manifest.json">

        <!-- for colour picker -->

        <script src="js/jscolor.min.js"></script>

    </head>

    <body>

        <div class="fullScreen centreContent noselect">

            <div class="sectionBox info">

                <h1>Melbourne Place</h1>

                <p>Things coming soon:</p>

                <ul>
                    <li>website-connected lights</li>
                    <li>live temperature data</li>
                    <li>party details</li>
                </ul>
                
            </div>

            <div class="sectionBox bell">

                <h1>Doorbell</h1>

                <p>Ring our real doorbell in our real house!</p>
                <button id ="bell" class="ringer">Ring!</button>
                
            </div>
            
            <div class="sectionBox lights">

                <h1>Lights</h1>

                <p>Control the LED strip in our living room.</p>

                <input value="FFA000" data-jscolor="{
                    preset: 'small dark',
                    position: 'top',
                    onChange:'setStaticColour(this.toHEXString())'
                }">

                <select id="preset" name="preset">

                    <option value="blank">blank</option>

                    <?php

                    $files = scandir("light-scripts");

                    foreach ($files as $file) {
                        echo sprintf("<option value=\"%s\">%s</option>", $file, $file);
                    }

                    ?>


                </select>
                
            </div>

        </div>

        <div id="overlay" class="fullScreen centreContent noselect overlay hidden">
            <div class="bellIconContainer"></div>
        </div>

        <script src="js/main.js"></script>
        <script src="js/led.js"></script>

    </body>

</html>
