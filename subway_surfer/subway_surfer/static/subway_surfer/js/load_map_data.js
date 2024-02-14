/***
 * Loads and displays map data
 * 
 * 
 */

window.displayTrainMarkers = function(){
        consol.log('hello')
        const dataElement = document.getElementById('data-fetcher');
        const trainInfo = JSON.parse(dataElement.getAttribute('data-trainInfo'));
        displayLocation(trainInfo);

}

function updateMarkers() {
    const agency = sessionStorage.getItem('agency');
    console.log(` agency: ${agency}`);
    fetch(`/map/${agency}/`)
    .then(response => console.log(response))
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(`Error fetching data ${error}`)
    });
}

//setInterval(updateMarkers, 5000);


function displayLocation(marker_data){
    trainLayer.clearLayers();
    Object.keys(marker_data).forEach(key => {
        console.log(key);
        let train = marker_data[key];
        console.log(train);
        displayTrainCurrentLoc(train, trainLayer);
  });
}


function displayTrainCurrentLoc(item, trainLayer) {
    let trainNumber = item.trainno;
    let trainMarker = L.marker([item.lat, item.lon]).addTo(trainLayer);
    trainLayer.addTo(map);
    let popup = L.popup({
        "autoClose": false,
        "closeOnClock": null
    }).setContent((
            `<b>Train No. </b> ${trainNumber}<br>
            <b>Next Stop: </b> ${item.nextstop} <br>
            <b>Line: </b> ${item.line}<br>
            <b> Destination: </b> ${item.dest}`));
    trainMarker.bindPopup(popup);
}