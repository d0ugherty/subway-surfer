/***
 * Loads and displays map data
 * 
 * 
 */

function displayMapMarkers() { 
    const agency = sessionStorage.getItem('agency');
    fetch(`/api/map_markers/${agency}/`)
        .then(response => response.json())
        .then(marker_data => {
            trainLayer.clearLayers();
            Object.keys(marker_data).forEach(key => {
                let train = marker_data[key];
                displayTrainCurrentLoc(train, trainLayer);
          });
        })
        .catch(error => console.error('Error fetching train data:', error));
}
setInterval(displayMapMarkers, 2000);

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

function displayShapes(shape_data) {
    Object.keys(shape_data).forEach(key => {

        let latlngs = [];
        let shape = shape_data[key];

        for(const point of shape) {
            latlngs.push([point.shape_pt_lat, point.shape_pt_lon]);
        }

        L.polyline(latlngs, { color: '#43647c'}).addTo(map);
    });
}