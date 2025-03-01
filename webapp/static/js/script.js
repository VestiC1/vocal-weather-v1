var weatherData;
var selectedDate;
var indexes = [];


document.getElementById('prev').addEventListener("click", function(){
    selectedDate.setDate(selectedDate.getDate() -1);
    computedIndexes();
    if (indexes.length == 0){
        selectedDate.setDate(selectedDate.getDate() + 1);
    }else{
        displayDate();
        displayTable();
    }
    displayDate();
   
})

document.getElementById('next').addEventListener("click", function(){
    
    selectedDate.setDate(selectedDate.getDate() + 1);
    computedIndexes();
    if (indexes.length == 0){
        selectedDate.setDate(selectedDate.getDate() - 1);
    }else{
        displayDate();
        displayTable();
    }
    displayDate();
})

function displayDate(){
    if (indexes.length > 0){
    const dateDiv = document.getElementById('date');
    dateDiv.innerHTML = selectedDate.toLocaleDateString("fr-FR") ;
    }
}

function computedIndexes(){
    indexes = [];
    let i = 0;
    weatherData.date.forEach( (date) => {
        parsedDate = new Date(date)
        if (selectedDate.getDate() == parsedDate.getDate()){
            indexes.push(i);
        }
        i++;
    });
}

document.addEventListener("DOMContentLoaded", function () {
    let SpeechSDK;
    let recognizer;

    const speechKey = document.querySelector('meta[name="speech-key"]').getAttribute('content');
    const speechRegion = document.querySelector('meta[name="speech-region"]').getAttribute('content');

    const startRecognizeOnceAsyncButton = document.getElementById("microphone-button");
    const phraseDiv = document.getElementById("recognized-text");
    

    startRecognizeOnceAsyncButton.addEventListener("click", function () {

        var speechConfig = SpeechSDK.SpeechConfig.fromSubscription(speechKey, speechRegion);

        startRecognizeOnceAsyncButton.disabled = true;
        phraseDiv.innerHTML = "";

        speechConfig.speechRecognitionLanguage = "fr-FR";
        var audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
        recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);

        recognizer.recognizeOnceAsync(
            function (result) {
                startRecognizeOnceAsyncButton.disabled = false;
                phraseDiv.innerHTML += result.text;
                window.console.log(result);

                sendVoiceCommand(result.text);

                recognizer.close();
                recognizer = undefined;
            },
            function (err) {
                startRecognizeOnceAsyncButton.disabled = false;
                phraseDiv.innerHTML += err;
                window.console.log(err);

                recognizer.close();
                recognizer = undefined;
            });
    });

    if (!!window.SpeechSDK) {
        SpeechSDK = window.SpeechSDK;
        startRecognizeOnceAsyncButton.disabled = false;
    }

});

function sendVoiceCommand(voiceCommand) {
    // Reset state
    selectedDate = undefined;
    weatherData  = undefined;
    fetch('/weather', { // Requête route '/weather'
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'voice_command=' + encodeURIComponent(voiceCommand)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Réponse du back-end:", data);
            displayWeatherInfo(data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête au back-end:', error);
            alert('Erreur lors de la récupération des données météo.');
        });
}



function displayTable(){
    computedIndexes();
    if (indexes.length > 0){
        const weatherTable = document.getElementById('weather-table');

        let j = 0;
        indexes.forEach((i) => {
            if (weatherTable.rows.length <25 ){
                let row = weatherTable.insertRow();
                let hour = row.insertCell(0);
                hour_stamp = new Date(weatherData.date[i]);
                hour.innerHTML = `${String(hour_stamp.getHours()).padStart(2, '0')}:${String(hour_stamp.getMinutes()).padStart(2, '0')}`;

                let temp = row.insertCell(1);
                temp.innerHTML = Math.round(weatherData.temperature_2m[i]);

                let cloud_cover = row.insertCell(2);
                cloud_cover.innerHTML = weatherData.cloud_cover[i];

                let hum = row.insertCell(3);
                hum.innerHTML = weatherData.relative_humidity_2m[i];

                let prec = row.insertCell(4);
                prec.innerHTML = weatherData.precipitation[i];

                let wind_speed = row.insertCell(5);
                wind_speed.innerHTML = Math.round(weatherData.wind_speed_10m[i]);
            }else {
                
                let hour =  weatherTable.rows[j+1].cells[0];
                hour_stamp = new Date(weatherData.date[i]);
                hour.innerHTML = `${String(hour_stamp.getHours()).padStart(2, '0')}:${String(hour_stamp.getMinutes()).padStart(2, '0')}`;

                let temp =  weatherTable.rows[j+1].cells[1];
                temp.innerHTML = Math.round(weatherData.temperature_2m[i]);

                let cloud_cover =  weatherTable.rows[j+1].cells[2];
                cloud_cover.innerHTML = weatherData.cloud_cover[i];

                let hum =  weatherTable.rows[j+1].cells[3];
                hum.innerHTML = weatherData.relative_humidity_2m[i];

                let prec =  weatherTable.rows[j+1].cells[4];
                prec.innerHTML = weatherData.precipitation[i].toFixed(2);

                let wind_speed =  weatherTable.rows[j+1].cells[5];
                wind_speed.innerHTML = Math.round(weatherData.wind_speed_10m[i]);
                j++;
            }
        });
    };

}

function displayWeatherInfo(data) {
    weatherData = data;
    console.log(weatherData);
    const mainWeatherInfoDiv = document.getElementById('weather-main');
    if ('error' in weatherData){
        const phraseDiv = document.getElementById("recognized-text");
        phraseDiv.innerHTML += `<br> <span class='text-danger'>${weatherData.error}</span>`
        weatherData = undefined;
        mainWeatherInfoDiv.classList.add('visually-hidden');
    }else{
       

        document.getElementById('city-name').textContent = weatherData.city;
        document.getElementById('temperature').textContent = weatherData.hourly_temperature_2m;
        document.getElementById('humidity').textContent = weatherData.hourly_relative_humidity_2m;
        document.getElementById('precipitation').textContent = weatherData.hourly_precipitation;
        document.getElementById('cloud-cover').textContent = weatherData.hourly_cloud_cover;
        document.getElementById('wind-speed').textContent = weatherData.hourly_wind_speed_10m;
        mainWeatherInfoDiv.classList.remove('visually-hidden');

        selectedDate = new Date(weatherData.date[0]);
        computedIndexes();
        displayDate();
        displayTable();
    }
   
    

    
   
}
