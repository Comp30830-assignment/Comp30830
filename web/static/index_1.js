
let heatmap;


function getStations() {
  fetch("/stations")
    .then((response) => response.json())
    .then((data) => {
      console.log("fetch response", typeof data);
      addMarkers(data);
      drawHeatmap(data); 
    });
}

function initMap() {
  
  google.charts.load('current', { packages: ['corechart'] });
  const dublin = { lat: 53.35014, lng: -6.266155 };
  // The map, centered at Dublin



  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: dublin,
    mapId: "60579be615b58573",//應用自定義樣式
    
  });
    const heatmapControlDiv = document.getElementById("heatmap-control");
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(heatmapControlDiv);

  getStations();
  //setInterval(getStations, 60 * 1000); // 每60秒获取一次实时数据
  // heatmap = new google.maps.visualization.HeatmapLayer();
  // heatmap.set("radius", 1800);
}


let currentInfoWindow = null;

function addMarkers(stations) {

  for (const station of stations) {
    const hoverIcon = {
      url: 'hover_marker.png',
      scaledSize: new google.maps.Size(60, 60), // 调整图标大小
      anchor: new google.maps.Point(33, 45), // 调整图标偏移
    };

    //console.log(station);
    const marker = new google.maps.Marker({
      position: {
        lat: station.position_lat,
        lng: station.position_lng,
      },
      map: map,
      title: station.name,
      station_number: station.number,
      animation: google.maps.Animation.DROP,//添加動畫效果
    });

    // 添加 mouseover 事件侦听器
    marker.addListener('mouseover', () => {
      marker.setIcon(hoverIcon);
    });
    // 添加 mouseout 事件侦听器
    marker.addListener('mouseout', () => {
      marker.setIcon(null); // 将图标设置为 null 以恢复默认图标
    });

    const contentString = '<div>' +
      '<h3 id="firstHeading" class="firstHeading">' + station.name + '</h3>' +
      '<p><strong>Station Address:   </strong>' + station.address + '</p>' +
      '<p><strong>Bike Stands:   </strong>' + station.bike_stands + '</p>' +
      '<p><strong>Bike Number:   </strong>' + station.number + '</p>' +
      '<p><strong>Business Status:   </strong>' + station.status + '</p>' +
      '<p><strong>View the Number of Bikes available historically</strong></p>' +
      '<input id="inputDate" type="text" placeholder="Enter date (YYYY-MM-DD)"/>' + // 添加输入框
      '<button id="btnLoadData" style="background-color: yellowgreen; color: white; border: none; padding: 5px 12px; font-size: 14px;">Search!</button>' + // 添加带有颜色设置、无边框且更大的按钮
// 添加带有颜色设置且无边框的按钮
 // 添加带有颜色设置的按钮
      '</div>';
    //const contentString =node;

    const infowindow = new google.maps.InfoWindow({
      content: contentString
    });

    marker.addListener("click", () => {
      if (currentInfoWindow) {
        currentInfoWindow.close(); // 关闭当前的信息窗口
      }

      // Clear the content of chart_div2 when a new marker is clicked
      document.getElementById('chart_div2').innerHTML = '';

      infowindow.open({
        anchor: marker,
        map,
      });
      currentInfoWindow = infowindow;

      google.maps.event.addListener(infowindow, 'domready', () => {
        document.getElementById("btnLoadData").addEventListener("click", () => {
          const inputDate = document.getElementById("inputDate").value;
          if (inputDate) {
            fetch("/occupancy2/" + marker.station_number + "/" + inputDate)
              .then(response => response.json())
              .then(data => {
                data = JSON.parse(data.data);
                const dataTable = new google.visualization.DataTable();

                dataTable.addColumn('string', 'Time of Day'); // 更改此处
                dataTable.addColumn('number', 'Available Bikes');

                data.forEach(row => {
                  const date = new Date(row[0]);
                  const hour = date.getHours();
                  const hourLabel = hour.toString().padStart(2, '0') + ":00";
                  dataTable.addRow([hourLabel, row[1]]);
                });

                const options = {
                  title: 'Available Bikes per Hour on ' + inputDate,
                  legend: 'none',
                  colors: ['#32CD32'],
                  hAxis: {
                    title: 'Time of Day',
                    slantedText: true,
                    slantedTextAngle: 45,
                    ticks: generateHourlyTicks()
                  },
                  vAxis: {
                    title: 'Number of Bikes'
                  },
                  animation: {
                    duration: 2000,
                    easing: "out",
                    startup: true,
                  }
                };
                const chart = new google.visualization.ColumnChart(document.getElementById('chart_div2'));
                chart.draw(dataTable, options);
              })
              .catch(error => console.log(error));
          } else {
            alert("Please enter a valid date.");
          }
        });
      });







      fetch("/occupancy/" + marker.station_number)
        .then(response => response.json())
        .then(data => {
          data = JSON.parse(data.data);
          const dataTable = new google.visualization.DataTable();
          var hAxisLabels = ["Mon", "Tues", "Wed", "Thrus", "Fri", "Sat", "Sun"];

          dataTable.addColumn('datetime', 'Time of Day');
          dataTable.addColumn('number', 'available_bikes');
          data.forEach(row => {
            dataTable.addRow([new Date(row[0]), row[1]]);
          });
          const options = {
            title: 'Average Bikes Available Per Day',
            legend: 'none',
            colors: ['#FFA500'], // 添加此行以设置橙黄色
            hAxis: {
              title: 'Day',
              format: 'M/d',
              gridlines: {
                count: 8, // 包括起始和結束日期，共顯示8個網格線
              },
              ticks: data.map(row => new Date(row[0])), // 創建一個日期數組作為橫坐標的刻度
              baselineColor: 'Transparent'
            },
            vAxis: {
              title: 'Number of Bikes'
            },
            animation: {
              duration: 2000,
              easing: "out",
              startup: true,
            }


          };
          const chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
          chart.draw(dataTable, options);
        })
        .catch(error => console.log(error));

    });
  }
}


function generateHourlyTicks() {
  const ticks = [];
  for (let i = 0; i < 24; i++) {
    const hourLabel = i.toString().padStart(2, '0') + ":00";
    ticks.push({ v: hourLabel, f: hourLabel }); // 修改此行
  }
  return ticks;
}
// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.


function drawHeatmap(stations) {
  const heatmapData = stations.map((station) => ({
    location: new google.maps.LatLng(station.position_lat, station.position_lng),
    weight: station.available_bikes,
  }));

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
    map: null,
  });
  var gradient = [ 'rgba(102, 204, 0, 0)',  'rgba(102, 204, 0, 1)',  'rgba(187, 255, 0, 1)',  'rgba(255, 238, 0, 1)',  'rgba(255, 153, 0, 1)',  'rgba(255, 102, 0, 1)',];

  heatmap.set("radius", 60); // 确保在这里设置正确的半径
  heatmap.set("opacity", 0.6); // 调整这个值以改变不透明度
  heatmap.set("gradient", gradient); // 指定一个自定义颜色渐变
}


function toggleHeatmap(checked) {
  if (checked) {
    let opacity = 0;
    heatmap.setMap(map);

    const fadeIn = setInterval(() => {
      opacity += 0.05;
      heatmap.set("opacity", opacity);

      if (opacity >= 0.6) {
        clearInterval(fadeIn);
      }
    }, 100);
  } else {
    let opacity = 0.6;

    const fadeOut = setInterval(() => {
      opacity -= 0.05;
      heatmap.set("opacity", opacity);

      if (opacity <= 0) {
        heatmap.setMap(null);
        clearInterval(fadeOut);
      }
    }, 100);
  }
}

document.getElementById("heatmap-toggle").addEventListener("change", (event) => {
  toggleHeatmap(event.target.checked);
});


var map = null;
window.initMap = initMap;

