var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {    
    zoom: 16,
    center: {lat: 42.374, lng: -71.117},
    mapTypeId: 'roadmap'
  });

  d3.csv("/harvardcrime/harvard_crime_incidents.csv", function(data) {
  console.log(data[0]);
  });
  
  function getMarkers() {
      let start = "<ul>";
      for (i = 0; i < data.length; i++) {  
        marker = new google.maps.Marker({
             position: new google.maps.LatLng(data[i][9], data[i][10]),
             map: map
            )};
        start += "<li><a href='" + data[i][0] + "' target='_blank'>" + "Incident type" + data[i][1] + "' target='_blank'>" + "Beginning of Occurrence" + data[i][2] + "' target='_blank'>"+ "Ending of Occurrence" + data[i][3] + "' target='_blank'>" + "Location" + data[i][4] + "' target='_blank'>" + "Address" + data[i][5] + "</a></li>
   }
        
    heatmap = new google.maps.visualization.HeatmapLayer({
          data: getPoints(),
          map: map
        });

    function toggleHeatmap() {
        heatmap.setMap(heatmap.getMap() ? null : map);
      }
    function changeGradient() {
        var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
        heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
      }
    
    function changeRadius() {
        heatmap.set('radius', heatmap.get('radius') ? null : 20);
      }

    function changeOpacity() {
        heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
      }
       
    function getPoints() {
        d = [];
        for (i = 0; i < data.length; i++) {
            d[i] = new google.maps.LatLng(data[i][9], data[i][10]);
        }
        return d;
     }
}
   
