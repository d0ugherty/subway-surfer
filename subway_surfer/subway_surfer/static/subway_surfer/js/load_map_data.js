

function load_loc_data(element_id){
    document.addEventListener('DOMContentLoaded', function() {
      var trainLocData = JSON.parse(document.getElementById(element_id).textContent);
      //return trainLocData;
      displayLocation(trainLocData);
    });
}

function displayLocation(data){
  data.forEach(element => console.log(element));
}

function displayTrainCurrentLoc(item, trainLayer, icon) {
  let trainNumber = item.trainno;
  let trainMarker = L.marker([item.lat, item.lon], {
      icon: icon
  }).addTo(trainLayer);
  trainLayer.addTo(map);
  let popup = L.popup({
      "autoClose": false,
      "closeOnClock": null
  }).setContent((`<b>Train No. </b> ${trainNumber}<br>
            <b>Next Stop: </b> ${item.nextstop} <br>
            <b>Line: </b> ${item.line}<br>
            <b> Destination: </b> ${item.dest}`));
  trainMarker.bindPopup(popup);
}