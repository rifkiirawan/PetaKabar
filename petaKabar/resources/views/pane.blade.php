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
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
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
<!-- <script src="{{ asset('data/kabupaten.js')}}"></script> -->
<script src="{{ asset('data/kabupaten1.js')}}"></script>
<script src="{{ asset('data/kelurahan.js')}}"></script>


<script>
    // var map = L.map('map').setView([-1.1697, 119.0879], 5);
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
    // var map = L.map('map');

    var map = L.map("map").setView([-7.460517719883772, 112.73071289062499], 6);

    // var tiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    //     maxZoom: 18,
    //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
    //         'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    //     id: 'mapbox/light-v9',
    //     tileSize: 512,
    //     zoomOffset: -1,
    //     minZoom: 6
    // }).addTo(map);

    var tiles = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 15,
        minZoom: 6,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(map);

    const bencanaP = L.icon({
        iconUrl: "{{ asset('icons/bencana_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const bencanaS = L.icon({
        iconUrl: "{{ asset('icons/bencana_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const bencanaT = L.icon({
        iconUrl: "{{ asset('icons/bencana_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kriminalP = L.icon({
        iconUrl: "{{ asset('icons/kriminal_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kriminalS = L.icon({
        iconUrl: "{{ asset('icons/kriminal_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kriminalT = L.icon({
        iconUrl: "{{ asset('icons/kriminal_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kesehatanT = L.icon({
        iconUrl: "{{ asset('icons/kesehatan_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kesehatanS = L.icon({
        iconUrl: "{{ asset('icons/kesehatan_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kesehatanP = L.icon({
        iconUrl: "{{ asset('icons/kesehatan_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const ekonomiT = L.icon({
        iconUrl: "{{ asset('icons/ekonomi_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const ekonomiS = L.icon({
        iconUrl: "{{ asset('icons/ekonomi_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const ekonomiP = L.icon({
        iconUrl: "{{ asset('icons/ekonomi_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const olahragaT = L.icon({
        iconUrl: "{{ asset('icons/olahraga_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const olahragaS = L.icon({
        iconUrl: "{{ asset('icons/olahraga_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const olahragaP = L.icon({
        iconUrl: "{{ asset('icons/olahraga_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kecelakaanT = L.icon({
        iconUrl: "{{ asset('icons/kecelakaan_t.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kecelakaanS = L.icon({
        iconUrl: "{{ asset('icons/kecelakaan_s.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    const kecelakaanP = L.icon({
        iconUrl: "{{ asset('icons/kecelakaan_p.png')}}",
        iconSize: [40, 40], // size of the icon
        iconAnchor: [2, 2], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -2] // point from which the popup should open relative to the iconAnchor
    });
    // var marker = L.marker([112.73242950439453, -7.3045794286997445], {
    //     icon: bencanaP
    // }).addTo(map).bindPopup('tes');
    // console.log(bencanaP);

    // $.getJSON("{{ asset('data/kelurahan.js')}}"),
    //     function(geoJSONdata) {
    //         var geoJSONgroup = L.geoJSON(geoJSONdata).addTo(map);
    //     }
    // L.geoJSON(kelurahan, {
    //     pointToLayer: function(feature, latlng) {
    //         return markers.addLayer(L.circleMarker(latlng, geoJSONMarkerOptions))
    //     }
    // }).addTo(map);

    // var marker1 = L.geoJson(kelurahan, {
    //     pointToLayer: function(feature, latlng) {
    //         return L.marker(latlng, {
    //             icon: bencanaP
    //         });
    //     }
    // });

    // var markers = new L.FeatureGroup();

    // markers.addLayer(marker1);

    // map.on('zoomend', function() {
    //     if (map.getZoom() > 10) {
    //         map.addLayer(markers);

    //     } else {
    //         map.removeLayer(markers);
    //     }
    // });

    var selectedLayerId = selectedLayerKabupatenId = selectedLayerKecamatanId = {};

    //provinsi
    var geojson = L.geoJson(data, {
        style: {
            weight: 2,
            opacity: 1,
            color: "white",
            dashArray: "3",
            fillOpacity: 0.7,
            fillColor: "#83d2ff"
        },
        onEachFeature: onEachFeature
    }).addTo(map);

    //kabupaten
    var geojson2 = L.geoJson(kabupaten1, {
        style: {
            weight: 2,
            opacity: 0,
            color: "white",
            dashArray: "3",
            fillOpacity: 0,
            fillColor: "#ff7800"
        },
        onEachFeature: onEachFeature2
    }).addTo(map);

    //kecamatan
    var geojson3 = L.geoJson(kelurahan, {
        pointToLayer: function(feature, latlng) {
            let icon;
            if (feature.properties.Kategori == "Bencana" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: bencanaT
                });
            } else if (feature.properties.Kategori == "Bencana" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: bencanaS
                });
            } else if (feature.properties.Kategori == "Bencana" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: bencanaP
                });
            } else if (feature.properties.Kategori == "Kriminalitas" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: kriminalT
                });
            } else if (feature.properties.Kategori == "Kriminalitas" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: kriminalS
                });
            } else if (feature.properties.Kategori == "Kriminalitas" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: kriminalP
                });
            } else if (feature.properties.Kategori == "Kesehatan" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: kesehatanT
                });
            } else if (feature.properties.Kategori == "Kesehatan" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: kesehatanS
                });
            } else if (feature.properties.Kategori == "Kesehatan" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: kesehatanP
                });
            } else if (feature.properties.Kategori == "Ekonomi" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: ekonomiT
                });
            } else if (feature.properties.Kategori == "Ekonomi" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: ekonomiS
                });
            } else if (feature.properties.Kategori == "Ekonomi" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: ekonomiP
                });
            } else if (feature.properties.Kategori == "Olahraga" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: olahragaT
                });
            } else if (feature.properties.Kategori == "Olahraga" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: olahragaS
                });
            } else if (feature.properties.Kategori == "Olahraga" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: olahragaP
                });
            } else if (feature.properties.Kategori == "Kecelakaan" && feature.properties.Jumlah < 50) {
                icon = L.marker(latlng, {
                    icon: kecelakaanT
                });
            } else if (feature.properties.Kategori == "Kecelakaan" && feature.properties.Jumlah > 50 && feature.properties.Jumlah < 100) {
                icon = L.marker(latlng, {
                    icon: kecelakaanS
                });
            } else if (feature.properties.Kategori == "Kecelakaan" && feature.properties.Jumlah > 100) {
                icon = L.marker(latlng, {
                    icon: kecelakaanP
                });
            }
            return icon
        },
        style: {
            opacity: 0,
            fillOpacity: 0
        },
        onEachFeature: onEachFeature3
    });

    var markers = new L.FeatureGroup();
    markers.addLayer(geojson3);


    function onEachFeature(feature, layer) {
        // console.log(layer);
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    function onEachFeature2(feature, layer) {
        layer.bindPopup('Kecamatan : ' + feature.properties.Kecamatan + '<br>Kategori : ' + feature.properties.Kategori + '<br>Jumlah : ' + feature.properties.Jumlah);
        layer.on({
            mouseover: highlightFeature2,
            mouseout: resetHighlight2,
            click: zoomToFeature2,
            add: (e) => e.target.bringToBack()
        });
    }

    function onEachFeature3(feature, layer) {
        layer.bindPopup('Kecamatan : ' + feature.properties.Kecamatan + '<br>Kategori : ' + feature.properties.Kategori + '<br>Jumlah : ' + feature.properties.Jumlah);
        layer.on({
            // mouseover: highlightFeature3,
            // mouseout: resetHighlight3,
            // click: zoomToFeature3,
            // add: (e) => e.target.bringToBack()
        });
    }

    function highlightFeature3(e) {
        console.log(selectedLayerKabupatenId);
        console.log(e.target.feature.properties.WADMPR);
        if (selectedLayerKabupatenId.id !== e.target._leaflet_id && selectedLayerId.provinsi == e.target.feature.properties.WADMPR) {
            var layer = e.target;
            layer.setStyle({
                weight: 2,
                color: "#ff7800",
                dashArray: "",
                fillOpacity: 0.7
            });
        }
    }

    function resetHighlight3(e) {
        if (selectedLayerKabupatenId.id !== e.target._leaflet_id && selectedLayerId.provinsi == e.target.feature.properties.WADMPR) {
            e.target.setStyle({
                weight: 2,
                opacity: 1,
                color: "white",
                dashArray: "3",
                fillOpacity: 0.7,
                fillColor: "#ff7800"
            });
        }
    }

    function zoomToFeature3(e) {
        toggleLayerVisibility3(map, e.target);
        geojson3.eachLayer(function(layer) {
            layer.bringToFront();
            console.log(layer.feature.properties.WADMPR);
            console.log(selectedLayerId.provinsi);
            if (layer.feature.properties.Kabupaten.toLowerCase() == selectedLayerKabupatenId.kabupaten.toLowerCase()) {
                // 
            } else if (layer.feature.properties.Kabupaten.toLowerCase() !== selectedLayerKabupatenId.kabupaten.toLowerCase()) {
                geojson2.resetStyle(layer);
            }
        });
    }

    function toggleLayerVisibility3(map, selectedLayer) {
        if (selectedLayerKecamatanId && selectedLayerKecamatanId.id !== selectedLayer._leaflet_id && selectedLayerKabupatenId.Kabupaten.toLowerCase() == e.target.feature.properties.Kabupaten.toLowerCase()) {
            map.eachLayer(layer => {
                if (layer._leaflet_id === selectedLayerKecamatanId.id) geojson2.resetStyle(layer);
            });
        }
        selectedLayer.setStyle({
            opacity: 0,
            fillOpacity: 0.0
        });
        selectedLayerKabupatenId = {
            id: selectedLayer._leaflet_id,
            kabupaten: selectedLayer.feature.properties.WADMPR
        }; //save identifier of a selected layer
    }

    function highlightFeature2(e) {
        console.log(selectedLayerKabupatenId);
        console.log(e.target.feature.properties.WADMPR);
        if (selectedLayerKabupatenId.id !== e.target._leaflet_id && selectedLayerId.provinsi == e.target.feature.properties.WADMPR) {
            var layer = e.target;
            layer.setStyle({
                weight: 2,
                color: "#ff7800",
                dashArray: "",
                fillOpacity: 0.7
            });
        }
    }

    function resetHighlight2(e) {
        if (selectedLayerKabupatenId.id !== e.target._leaflet_id && selectedLayerId.provinsi == e.target.feature.properties.WADMPR) {
            e.target.setStyle({
                weight: 2,
                opacity: 1,
                color: "white",
                dashArray: "3",
                fillOpacity: 0.7,
                fillColor: "#ff7800"
            });
        }
    }

    function zoomToFeature2(e) {
        map.fitBounds(e.target.getBounds(), {
            maxZoom: 15
        });
        toggleLayerVisibility2(map, e.target);
    }

    function toggleLayerVisibility2(map, selectedLayer) {
        if (selectedLayerKabupatenId && selectedLayerKabupatenId.id !== selectedLayer._leaflet_id && selectedLayerId.provinsi == selectedLayer.feature.properties.WADMPR) {
            map.eachLayer(layer => {
                if (layer._leaflet_id === selectedLayerKabupatenId.id) geojson2.resetStyle(layer);
            });
        }
        selectedLayer.setStyle({
            opacity: 0,
            fillOpacity: 0.0
        });
        console.log("ab");
        selectedLayerKabupatenId = {
            id: selectedLayer._leaflet_id,
            kabupaten: selectedLayer.feature.properties.WADMPR
        }; //save identifier of a selected layer
    }

    function highlightFeature(e) {
        if (selectedLayerId.id !== e.target._leaflet_id) {
            var layer = e.target;
            layer.setStyle({
                weight: 2,
                color: "#07C0FF",
                dashArray: "",
                fillOpacity: 0.55
            });
        }
    }

    function resetHighlight(e) {
        if (selectedLayerId.id !== e.target._leaflet_id) {
            geojson.resetStyle(e.target);
            // geojson2.eachLayer(function(layer) {
            //     console.log(layer.feature.properties.WADMPR);
            //     console.log(selectedLayerId.provinsi);
            //     if (layer.feature.properties.WADMPR !== selectedLayerId.provinsi) {
            //         geojson2.resetStyle(layer);
            //     }
            // });
        }
    }

    function zoomToFeature(e) {
        map.fitBounds(e.target.getBounds(), {
            maxZoom: 8
        });
        console.log("tes");
        // map.setZoom(8);
        toggleLayerVisibility(map, e.target);
        geojson2.eachLayer(function(layer) {
            layer.bringToFront();
            console.log(layer.feature.properties.WADMPR);
            console.log(selectedLayerId.provinsi);
            if (layer.feature.properties.WADMPR == selectedLayerId.provinsi) {
                layer.setStyle({
                    weight: 2,
                    opacity: 1,
                    color: "white",
                    dashArray: "3",
                    fillOpacity: 0.7,
                    fillColor: "#ff7800"
                });
            } else if (layer.feature.properties.WADMPR !== selectedLayerId.provinsi) {
                geojson2.resetStyle(layer);
            }
        });
    }

    function toggleLayerVisibility(map, selectedLayer) {
        if (selectedLayerId && selectedLayerId.id !== selectedLayer._leaflet_id) {
            map.eachLayer(layer => {
                if (layer._leaflet_id === selectedLayerId.id) geojson.resetStyle(layer);
            });
        }
        selectedLayer.setStyle({
            opacity: 0,
            fillOpacity: 0.0
        });
        selectedLayerId = {
            id: selectedLayer._leaflet_id,
            provinsi: selectedLayer.feature.properties.NAME_1
        }; //save identifier of a selected layer
    }

    map.on('zoomend', function(e) {
        var zoomLevel = map.getZoom();
        if (zoomLevel > 10) {
            map.addLayer(markers);
        } else {
            map.removeLayer(markers);
        }
        // if (zoomLevel < 9 && zoomLevel >= 6 && selectedLayerId == null) {
        //     //then toggle vibility or add/remove the desired layers
        //     // console.log(zoomLevel);
        //     geojson.eachLayer(function(layer) {
        //         if (selectedLayerId == layer._leaflet_id) {
        //             geojson.resetStyle(layer);
        //         }
        //     });
        // } else if (zoomLevel < 8 && zoomLevel >= 6 && selectedLayerId != null) {
        //     //Do the opposite
        //     // console.log(zoomLevel);
        //     geojson.eachLayer(function(layer) {
        //         if (selectedLayerId == layer._leaflet_id) {
        //             geojson.resetStyle(layer);
        //         }
        //     });
        // }
        // } else if (zoomLevel >= 8 && selectedLayerId != null) {
        //     geojson2.bringToFront();
        //     geojson2.setStyle({
        //         weight: 2,
        //         opacity: 1,
        //         color: "white",
        //         dashArray: "3",
        //         fillOpacity: 0.7,
        //         fillColor: "#ff7800"
        //     });
        // } else if (zoomLevel < 12 && zoomLevel >= 8 && selectedLayerId != null) {
        //     //Do the opposite
        //     // console.log(zoomLevel);
        //     geojson2.bringToFront();
        //     geojson.eachLayer(function(layer) {
        //         if (selectedLayerId == layer._leaflet_id) {
        //             geojson.resetStyle(layer);
        //         }
        //     });
        //     geojson2.eachLayer(function(layer) {
        //         if (selectedLayerKabupatenId == layer._leaflet_id) {
        //             geojson2.resetStyle(layer);
        //         }
        //     });
        // }

        console.log(zoomLevel);
    });



    map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');


    var legend = L.control({
        position: 'bottomright'
    });

    legend.onAdd = function(map) {

        var div = L.DomUtil.create('div', 'info legend');
        var grades = [0, 10, 20, 50, 100, 200, 500, 1000];
        var labels = [];
        var from, to;

        for (var i = 0; i < grades.length; i++) {
            from = grades[i];
            to = grades[i + 1];

            labels.push(
                '<i style="background:' + getColor(from + 1) + '"></i> ' +
                from + (to ? '&ndash;' + to : '+'));
        }

        div.innerHTML = labels.join('<br>');
        return div;
    };

    legend.addTo(map);

    // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);


    //     geoJSONgroup.eachLayer(function(layer) {
    //         if (layer.feature.properties.name === "Surabaya") {
    //             map.fitBounds(layer.getBounds());
    //         }
    //     });
    // });

    // map.setView({
    //     lat: -1.1697,
    //     lng: 119.0879
    // }, 4);

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
    // L.geoJSON(kelurahan, {
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