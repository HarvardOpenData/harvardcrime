var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {    zoom: 16,
    center: {lat: 42.374, lng: -71.117},
    mapTypeId: 'roadmap'
  });

  var markers = crime_data.map(function(crime_row) {
    return new google.maps.Marker({
      position: LatLng(crime_row),
      map: map,
      title: crime_row[crime_data_index["Incident Type"]]
    });
  });
}
