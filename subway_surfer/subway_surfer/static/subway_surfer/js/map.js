/***************
 *  Map creation using the Leaflet JavaScript library
 * 
 *  'stationLayer' and 'trainLayer' were created so markers can be added to layer groups rather than
 *   the map itself. This makes for easy marker removal either for toggling or 
 *   the retrieval of new data (live updating)
 * 
 *  TO DO: Modularize this
 * */


const map = L.map('map', {
    center: [39.952325, -75.163705],
    zoom: 11,
    layers: [
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png'),
      //  L.tileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png')
    ],
        tap: false
    });
    
map.attributionControl.addAttribution('Data <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>'+ 
                                    ' Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a>'+
                                    ' <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a>');

const trainLayer = L.layerGroup();
const stationLayer = L.layerGroup().addTo(map);
const trolleyLayer = L.layerGroup().addTo(map);
const trolleyStopLayer = L.layerGroup().addTo(map);
