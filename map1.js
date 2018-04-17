var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: {lat: 42.374, lng: -71.117},
    mapTypeId: 'roadmap'
  });

  function getMarkers() {
      d3.csv("https://raw.githubusercontent.com/HarvardOpenData/harvardcrime/master/harvard_crime_incidents.csv", function(data) {
        var infowindow = new google.maps.InfoWindow();
          for (i = 0; i < data.length; i++) {
            marker = new google.maps.Marker({
                 position: new google.maps.LatLng(data[i]["latitude"], data[i]["longitude"]),
                 map: map
            });

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infowindow.setContent(data[i]["incident_type"]);
                    infowindow.open(map, marker);
                }
            })(marker, i));

          }
      });
  }

  getMarkers()
}
