/***
 * Loads and displays map data
 * 
 * 
 */

function load_loc_data(element_id){
    document.addEventListener('DOMContentLoaded', function() {
      var trainLocData = JSON.parse(document.getElementById(element_id).textContent);
      displayLocation(trainLocData);
    });
}

function displayLocation(data){
  // Check if data itself is an array
  Object.keys(data).forEach(key => {
    let train = data[key];
    console.log('train number: ${key}', train);
    console.log('train number: ${key}', train.lat);
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