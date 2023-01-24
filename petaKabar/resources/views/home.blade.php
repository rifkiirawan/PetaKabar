<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web GIS</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css" integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ==" crossorigin="" />
    <link rel="stylesheet" href="{{ asset('leaflet/css/MarkerCluster.css')}}">
    <link rel="stylesheet" href="{{ asset('leaflet/css/MarkerCluster.Default.css')}}">
    <!-- Make sure you put this AFTER Leaflet's CSS -->
    <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js" integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ==" crossorigin=""></script>

    <style>
        #map {
            height: 950px;
            width: 100%;
        }
    </style>
</head>

<body>
    <div id="map"></div>
</body>

<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/"></script>
<script type="text/javascript" src="{{ asset('leaflet/js/leaflet.ajax.min.js')}}"></script>
<script type="text/javascript" src="{{ asset('leaflet/js/leaflet.markercluster.js')}}"></script>
<script src="{{ asset('data/data.js')}}"></script>

<script>
    var map = L.map('map').setView([-1.1697, 119.0879], 5);
    // L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoicnl1a2F6dWFzIiwiYSI6ImNrajJ6cDRhdDBoYmEyem5seG1hMnoyOGwifQ.LYTAS8IvX4_f-UpsE6-hJg', {
    //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    //     maxZoom: 18,
    //     id: 'mapbox/streets-v11',
    //     tileSize: 512,
    //     zoomOffset: -1,
    //     accessToken: 'pk.eyJ1Ijoicnl1a2F6dWFzIiwiYSI6ImNrajJ6cDRhdDBoYmEyem5seG1hMnoyOGwifQ.LYTAS8IvX4_f-UpsE6-hJg',
    //     center: [117.68554687499999,
    //         -2.284550660236957
    //     ]
    // }).addTo(map);

    var positronLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png', {
        attribution: '©OpenStreetMap, ©CartoDB',
        pane: 'labels'
    }).addTo(map);

    //street
    L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(map);

    map.createPane('labels');
    map.getPane('labels').style.zIndex = 650;
    map.getPane('labels').style.pointerEvents = 'none';
    var geojson = L.geoJson(GeoJsonData, geoJsonOptions).addTo(map);
    geojson.eachLayer(function(layer) {
        layer.bindPopup(layer.feature.properties.name);
    });

    map.fitBounds(geojson.getBounds());

    // const geoJSONMarkerOptions = {
    //     radius: 8,
    //     fillColor: "#ff7800",
    //     color: "#000",
    //     weight: 1,
    //     opacity: 1,
    //     fillOpacity: 0.8
    // };

    // const lightData = L.geoJSON(data, {
    //     onEachFeature: function(feature, layer) {
    //         const popupContent =
    //             '<h4 class = "text-primary">Street Light</h4>' +
    //             '<div class="container"><table class="table table-striped">' +
    //             "<thead><tr><th>Properties</th><th>Value</th></tr></thead>" +
    //             "<tbody><tr><td> Kecamatan </td><td>" +
    //             feature.properties.Kecamatan +
    //             "</td></tr>" +
    //             "<tr><td>Kategorivation </td><td>" +
    //             feature.properties.Kategori +
    //             "</td></tr>" +
    //             "<tr><td> Jumlah (watt) </td><td>" +
    //             feature.properties.Jumlah +
    //             "</td></tr>";
    //         layer.bindPopup(popupContent);

    //     },
    //     pointToLayer: function(feature, latlng) {
    //         return L.circleMarker(latlng, geoJSONMarkerOptions);
    //     },
    // });

    // const markers = L.markerClusterGroup().addLayer(lightData);
    // map.addLayer(markers);


    // var markers = L.markerClusterGroup();
    // //load geojson data
    // L.geoJSON(data, {
    //     pointToLayer: function(feature, latlng) {
    //         return markers.addLayer(L.circleMarker(latlng, geoJSONMarkerOptions))
    //     }
    // }).addTo(map);

    // // markers.addLayer(L.marker(getRandomLatLng(map)));
    // //clustermarker
    // // ... Add more layers ...
    // map.addLayer(markers);



    // var marker = L.marker([-7.2763092, 112.7932312]).addTo(map);

    // var polygon = L.polygon([
    //     [-7.2675746, 112.7929307],
    //     [-7.2789737, 112.8242218],
    //     [-7.2868796, 112.7601026, 15]
    // ]).addTo(map);

    // var lyrTrees;
    // var lyrClusterTrees;

    // lyrTrees = L.geoJSON.ajax("{{ asset('data/merged.geojson')}}", {
    //     pointToLayer: funReturnTrees
    // });
    // lyrTrees.on('data:loaded', function() {
    //     map.fitBounds(lyrTrees.getBounds());
    //     lyrClusterTrees.addLayer(lyrTrees);
    //     lyrClusterTrees.addTo(map);
    // })

    //function on trees layer
    // function funReturnTrees(latlng) {
    //     return L.circleMarker(latlng, {
    //         radius: 18,
    //         color: 'green'
    //     });
    // }
    // lyrClusterTrees = L.markerClusterGroup();
</script>

</html>