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


function displayLocation(data){
  // Check if data itself is an array
    Object.keys(data).forEach(key => {
        let train = data[key];
        displayTrainCurrentLoc(train, trainLayer);
  });
}


function displayTrainCurrentLoc(item, trainLayer) {
    trainLayer.clearLayers();
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

function displayShapes(shape_data) {
    for(let index=0; index <= shape_data.length; index++) {
        let shape = shape_data[i];
        console.log(shape.shape_pt_lat);
    }
}