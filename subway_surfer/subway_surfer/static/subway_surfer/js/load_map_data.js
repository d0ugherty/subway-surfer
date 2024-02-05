

function load_loc_data(element_id){
    document.addEventListener('DOMContentLoaded', function() {
      var trainLocData = JSON.parse(document.getElementById(element_id).textContent);
      console.log(trainLocData);
  });
}