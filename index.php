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
                    <li>live temperature data</li>
                    <li>party details</li>
                </ul>

                <p><i style="font-size: 80%">Contact billy@melbourneplace.net with any queries.</i></p>
                
            </div>

            <div class="sectionBox bell">

                <h1>Doorbell</h1>

                <p>Ring our real doorbell in our real house!</p>
                <button id="bell" class="ringer">Ring!</button>

                <div style="margin-top: 8px;">
                    <input type="text" id="morseMessage"></input>
                    <button id="sendMorse">Send</button>
                </div>
                
            </div>
            
            <div class="sectionBox lights">

                <h1>Lights</h1>

                <p>Control the LED strip in our living room.</p>

                <button class="colourPicker" data-jscolor="{
                    preset: 'small dark',
                    position: 'top',
                    onChange:'setStaticColour(this.toHEXString())'
                }">Select Static Colour</button>

                <div style="margin-top: 8px;">
                    <span>Preset:</span>
                    <select class="presetPicker" id="preset" name="preset" class="presetButton" onchange="setPreset(this.value)">

                        <?php

                        $allFiles = scandir("light-scripts"); // Or any other directory
                        $files = array_diff($allFiles, array('.', '..'));

                        foreach ($files as $file) {

                            $filenameNoExtension = pathinfo($file, PATHINFO_FILENAME);
                            echo sprintf("<option value=\"%s\">%s</option>", $file, $filenameNoExtension);

                        }

                        ?>


                    </select>
                </div>
                
            </div>

        </div>

        <div id="overlay" class="fullScreen centreContent noselect overlay hidden">
            <div class="bellIconContainer"></div>
        </div>

        <script src="js/doorbell.js"></script>
        <script src="js/led.js"></script>
        <script src="js/main.js"></script>

    </body>

</html>
