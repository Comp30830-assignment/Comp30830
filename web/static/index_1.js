// Initialize and add the map
// function initMap() {
//     const dublin = { lat: 53.350140, lng: -6.266155 };
//     // The map, centered at Dublin
//     map = new google.maps.Map
//         (document.getElementById("map"), {
//             zoom: 12,center: dublin,
//         });
//     // The marker, positioned at Dublin
//     const marker = new google.maps
//         .Marker({
//             position: dublin
//             ,map: map
//             ,
//         });
// }
// var map;
// window.initMap = initMap;



function addMarkers(stations) {
    for (const station of stations) {
        //console.log(station);
        const marker = new google.maps.Marker({
            position: {
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
        });

        const options = {
          title: "Occupancy Chart",
          hAxis: {
            title: "Time of Day",
            format: "MMM d, yyyy h:mm:ss a"
          },
          vAxis: {
            title: "Occupancy"
          }
        };

        var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number, function(data) {
            data = JSON.parse(data.data);
            console.log('data', data);    
            var node = document.createElement('div'),
            infowindow = new google.maps.InfoWindow(),
            chart = new google.visualization.ColumnChart(node);
            var chart_data = new google.visualization.DataTable();
            chart_data.addColumn('datetime', 'Time of Day');
            chart_data.addColumn('number', '#');
            _.forEach(data, function(row){chart_data.addRow([new Date(row[0]), row[1]]);})
            chart.draw(chart_data, options);
            infowindow.setContent(node);
            infowindow.open(marker.getMap(), marker);
        }).fail(function() {
            console.log( "error" );
        })

        // const contentString = '<div>' +
        // '<h3 id="firstHeading" class="firstHeading">'+station.name+'</h3>' +
        // '<p><strong>Station Address:   </strong>'+station.address+'</p>' +
        // '<p><strong>Bike Stands:   </strong>'+station.bike_stands+'</p>' +
        // '<p><strong>Bike Number:   </strong>'+station.number+'</p>' +
        // '<p><strong>Business Status:   </strong>'+station.status+'</p>' +
        // '</div>';
        // const contentString =node;

        // const infowindow = new google.maps.InfoWindow({
        //   content: contentString
        // });

        // marker.addListener("click", () => {
        //   infowindow.open({
        //     anchor: marker,
        //     map,
        //   });
        // });       
    }
}



function getStations() {
    fetch("/stations")
        .then((response) => response.json())
        .then((data) => {
            console.log("fetch response", typeof data);
            addMarkers(data);
        });
}


// // Initialize and add the map
// function initMap() {
//     const dublin = { lat: 53.35014, lng: -6.266155 };
//     // The map, centered at Dublin
//     map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 14,
//         center: dublin,
//     });
//     // const marker = new google.maps.Marker({
//     // position: dublin,
//     // map: map,
//     // });
//     getStations();
// }
// var map = null;
// window.initMap = initMap;

// var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number, 
// function(data) {
// data = JSON.parse(data.data);
// console.log('data', data);
// var node = document.createElement('div'),
// infowindow = new google.maps.InfoWindow(),
// chart = new google.visualization.ColumnChart(node);
// var chart_data = new google.visualization.DataTable();
// chart_data.addColumn('datetime', 'Time of Day');
// chart_data.addColumn('number', '#');
// _.forEach(data, function(row){
// chart_data.addRow([new Date(row[0]), row[1]]);
// })
// chart.draw(chart_data, options);
// infowindow.setContent(node);
// infowindow.open(marker.getMap(), marker);
// }).fail(function() {
// console.log( "error" );
// })



// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.
function initMap() {
    const dublin = { lat: 53.35014, lng: -6.266155 };
    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });
    getStations();
    const contentString =
    '<div id="content">' +
    '<div id="siteNotice">' +
    "</div>" +
    '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
    '<div id="bodyContent">' +
    "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
    "sandstone rock formation in the southern part of the " +
    "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) " +
    "south west of the nearest large town, Alice Springs; 450&#160;km " +
    "(280&#160;mi) by road. Kata Tjuta and Uluru are the two major " +
    "features of the Uluru - Kata Tjuta National Park. Uluru is " +
    "sacred to the Pitjantjatjara and Yankunytjatjara, the " +
    "Aboriginal people of the area. It has many springs, waterholes, " +
    "rock caves and ancient paintings. Uluru is listed as a World " +
    "Heritage Site.</p>" +
    '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">' +
    "https://en.wikipedia.org/w/index.php?title=Uluru</a> " +
    "(last visited June 22, 2009).</p>" +
    "</div>" +
    "</div>";

  const infowindow2 = new google.maps.InfoWindow({
    content: contentString,
    ariaLabel: "Uluru",
  });

  const marker2 = new google.maps.Marker({
    position: dublin,
    map,
  });

  marker2.addListener("click", () => {
    infowindow2.open({
      anchor: marker2,
      map,
    });
  });

  infoWindow2.addListener('closeclick', ()=>{
    // Handle focus manually.
  })
}


var map = null;
window.initMap = initMap;

