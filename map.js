var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {    
    zoom: 16,
    center: {lat: 42.374, lng: -71.117},
    mapTypeId: 'roadmap'
  });
  
  function getMarkers() {
      let start = "<ul>";
      d3.csv("https://raw.githubusercontent.com/HarvardOpenData/harvardcrime/master/harvard_crime_incidents.csv", function(data) {
          for (i = 0; i < data.length; i++) {
            marker = new google.maps.Marker({
                 position: new google.maps.LatLng(data[i][9], data[i][10]),
                 map: map
            });
            start += "<li><a href='" + data[i][0] + "' target='_blank'>" + "Incident type" + data[i][1] + "' target='_blank'>" + "Beginning of Occurrence" + data[i][2] + "' target='_blank'>"+ "Ending of Occurrence" + data[i][3] + "' target='_blank'>" + "Location" + data[i][4] + "' target='_blank'>" + "Address" + data[i][5] + "</a></li>";
          }
      });
  }
}
