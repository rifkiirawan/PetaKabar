<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Peta Kabar</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css" integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ==" crossorigin="" />
    <link rel="stylesheet" href="{{ asset('leaflet/css/MarkerCluster.css')}}">
    <link rel="stylesheet" href="{{ asset('leaflet/css/MarkerCluster.Default.css')}}">
    <link rel="stylesheet" href="{{ asset('leaflet/css/style.css')}}">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    <!-- Make sure you put this AFTER Leaflet's CSS -->
    <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js" integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ==" crossorigin=""></script>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="http://127.0.0.1:8000">Peta Kabar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse " id="navbarNavAltMarkup">
                <div class="navbar-nav ms-auto">
                    <a class="btn btn-primary me-2" href="http://127.0.0.1:8000/tabel">Lihat Semua Berita!</a>

                    {{-- <a class="nav-link" href="http://127.0.0.1:8000/scrap" onclick="return confirm('Program ini membutuhkan waktu beberapa menit untuk dijalankan, mohon tunggu hingga muncul pesan yang menunjukkan proses scraping telah dijalankan')">Jalankan Scraping</a> --}}

                    <!-- Button trigger modal -->
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#confirmationModal">
                        Jalankan Scraping
                    </button>

                    <!-- Modal -->
                    <div class="modal fade" id="confirmationModal" tabindex="-1" aria-labelledby="confirmationModalLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="confirmationModalLabel">Konfirmasi</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    Program ini membutuhkan waktu beberapa menit untuk dijalankan, mohon tunggu hingga muncul pesan yang menunjukkan proses scraping telah dijalankan
                                </div>
                                <div class="modal-footer">
                                    <a class="btn btn-primary" href="http://127.0.0.1:8000/scrap">Ya, jalankan</a>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    @if ($check == 1)
        <div class="alert alert-danger alert-dismissible fade show mb-0" role="alert">
            {{ $message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    @elseif ($check == 2)
        <div class="alert alert-success alert-dismissible fade show mb-0" role="alert">
            {{ $message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    @endif

    <!-- filter berita -->
    <div id="map" style="width: 100%; position:absolute">
        <div id="refreshButton" >
            <span id="filter_source" hidden>{{ $source }}</span>
            <span id="filter_range" hidden>{{ $range }}</span>

            <form action="{{route('filterMap')}}" method="POST">
                @csrf

                <div class="form-group mb-3">
                    <label for="sourceSelect">Sumber</label>
                    <select class="form-control" id="sourceSelect" name="source">
                        <option value="all" {{ ( $source == "all") ? 'selected' : '' }}>Semua</option>
                        <option value="www.kompas.com" {{ ( $source == "www.kompas.com") ? 'selected' : '' }}>Kompas</option>
                        <option value="www.tribunnews.com" {{ ( $source == "www.tribunnews.com") ? 'selected' : '' }}>Tribun News</option>
                        <option value="www.tempo.co" {{ ( $source == "www.tempo.co") ? 'selected' : '' }}>Tempo</option>
                        <option value="www.detik.com" {{ ( $source == "www.detik.com") ? 'selected' : '' }}>Detik</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="rangeSelect">Tanggal Berita</label>
                    <select class="form-control" id="rangeSelect" name="range">
                        <option value="all" {{ ( $range == "all") ? 'selected' : '' }}>Semua</option>
                        <option value="year" {{ ( $range == "year") ? 'selected' : '' }}>1 Tahun</option>
                        <option value="month" {{ ( $range == "month") ? 'selected' : '' }}>1 Bulan</option>
                        <option value="week" {{ ( $range == "week") ? 'selected' : '' }}>1 Minggu</option>
                        <option value="day" {{ ( $range == "day") ? 'selected' : '' }}>1 Hari</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="topicSelect">Topik Berita</label>
                    <select class="form-control" id="topicSelect" name="topic">
                        <option value="all" {{ ( $topic == "all") ? 'selected' : '' }}>Semua</option>
                        <option value="1" {{ ( $topic == "1") ? 'selected' : '' }}>Bencana</option>
                        <option value="2" {{ ( $topic == "2") ? 'selected' : '' }}>Ekonomi</option>
                        <option value="3" {{ ( $topic == "3") ? 'selected' : '' }}>Kecelakaan</option>
                        <option value="4" {{ ( $topic == "4") ? 'selected' : '' }}>Kesehatan</option>
                        <option value="5" {{ ( $topic == "5") ? 'selected' : '' }}>Kriminalitas</option>
                        <option value="6" {{ ( $topic == "6") ? 'selected' : '' }}>Olahraga</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Filter Berita</button>
            </form>
        </div>
        <!-- <button id="beritaButton" >
            <a href="http://127.0.0.1:8000/tabel" style="text-decoration: none; color: black;">Lihat Semua Berita!</a>
        </button> -->
    </div>

</body>

<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/"></script>
<script type="text/javascript" src="{{ asset('leaflet/js/leaflet.ajax.min.js')}}"></script>
<script type="text/javascript" src="{{ asset('leaflet/js/leaflet.markercluster.js')}}"></script>
<script src="{{ asset('data/kab.js')}}"></script>
<script src="{{ asset('data/prov.js')}}"></script>
<script src="{{ asset('data/kecamatan.js')}}"></script>

<script>
    var filter_source = "all";
    var filter_range = "all";

    if (document.getElementById("filter_source").innerText == "www.kompas.com") {
        filter_source = "kompas";
    }
    else if (document.getElementById("filter_source").innerText == "www.tribunnews.com") {
        filter_source = "tribun";
    }
    else if (document.getElementById("filter_source").innerText == "www.tempo.co") {
        filter_source = "tempo";
    }
    else if (document.getElementById("filter_source").innerText == "www.detik.com") {
        filter_source = "detik";
    }

    if (document.getElementById("filter_range").innerText == "year") {
        filter_range = "year";
    }
    else if (document.getElementById("filter_range").innerText == "month") {
        filter_range = "month";
    }
    else if (document.getElementById("filter_range").innerText == "week") {
        filter_range = "week";
    }
    else if (document.getElementById("filter_range").innerText == "day") {
        filter_range = "day";
    }

    // inisiasi map
    var map = L.map("map").setView([-3.0966358718415505, 118.21289062499999], 6);

    var tiles = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
        maxZoom: 11,
        minZoom: 6,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(map);

    var dataApi = {!! json_encode($response) !!}
    // console.log(dataApi);

    let kabupaten = [],
        provinsi = [];

    function hitungBerita(levelAdministrasi){
        var helper = {};
        var result = dataApi.reduce(function(r, o) {
            var key;
            if(levelAdministrasi == "kecamatan" && o.kecamatan && o.kecamatan != "-"){
                key = o.kecamatan;
                // console.log(o.kecamatan)
            } else if(levelAdministrasi == "kabupaten" && o.kabupaten && o.kabupaten != "-"){
                key =  o.kabupaten ;
            } else if(levelAdministrasi == "provinsi" && o.provinsi && o.provinsi != "-"){
                key = o.provinsi;
            } else {
                return r;
            }
            if(!helper[key]) {
                helper[key] = {
                    kategori: {},
                };
                if (levelAdministrasi == 'provinsi'){
                    helper[key].provinsi = o.provinsi
                } else if (levelAdministrasi == 'kabupaten'){
                    helper[key].kabupaten = o.kabupaten
                    helper[key].provinsi = o.provinsi
                } else if (levelAdministrasi == 'kecamatan'){
                    helper[key].kecamatan = o.kecamatan
                    helper[key].kabupaten = o.kabupaten
                    helper[key].provinsi = o.provinsi
                }
                helper[key].kategori[o.kategori] = {
                    keparahan: {}
                }
                helper[key].kategori[o.kategori].keparahan[o.tingkat_keparahan] = 1
                r.push(helper[key]);
            } else {
                if(o.kategori in helper[key].kategori){
                    if(!(o.tingkat_keparahan in helper[key].kategori[o.kategori].keparahan)){
                        helper[key].kategori[o.kategori].keparahan[o.tingkat_keparahan] = 1
                    } else {
                        helper[key].kategori[o.kategori].keparahan[o.tingkat_keparahan] += 1
                    }
                } else {
                    helper[key].kategori[o.kategori] = {
                        keparahan: {}
                    }
                    helper[key].kategori[o.kategori].keparahan[o.tingkat_keparahan] = 1
                }
                if(["kabupaten", "kecamatan"].includes(levelAdministrasi) && o.provinsi != '-' && helper[key].provinsi == '-'){
                    helper[key].provinsi = o.provinsi
                }
                if(levelAdministrasi == "kecamatan" && o.kabupaten != '-' && helper[key].kabupaten == '-'){
                    helper[key].kabupaten = o.kabupaten
                }
            }
            return r;
        }, []);
        console.log(result)
        return result;
    }
    var beritaKecamatan = hitungBerita("kecamatan");
    var beritaKabupaten = hitungBerita("kabupaten");
    var beritaProvinsi = hitungBerita("provinsi");
    // console.log(beritaProvinsi)

    //kecamatan
    var geojson3 = L.geoJson(dataKecamatan, {
        style: {
            opacity: 0,
            fillOpacity: 0
        },
        onEachFeature: onEachFeature3,
        filter: function(feature){
            if(beritaKecamatan.filter(k => k?.kecamatan.toLowerCase() == feature.properties.kecamatan.toLowerCase()).length > 0){
                return true
            }
        }
    });
    var geojson3MarkerOptions = {
            radius: 20,
            fillColor: "#F2DF3A",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.7
        };
    var geojson3Circle = L.geoJson(dataKecamatan, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, geojson3MarkerOptions);
        },
        filter: function(feature){
            if(beritaKecamatan.filter(k => k?.kecamatan.toLowerCase() == feature.properties.kecamatan.toLowerCase()).length > 0){
                return true
            }
        }
    });
    var markersKecamatan = new L.FeatureGroup();
    markersKecamatan.addLayer(geojson3);
    var markersKecamatanCircle = new L.FeatureGroup();
    markersKecamatanCircle.addLayer(geojson3Circle);

    //kabupaten
    var geojson2 = L.geoJson(dataKabupaten, {
        style: {
            opacity: 0,
            fillOpacity: 0
        },
        onEachFeature: onEachFeature2,
        filter: function(feature){
            if(beritaKabupaten.filter(k => k?.kabupaten.toLowerCase() == feature.properties.kabupaten.toLowerCase()).length > 0){
                return true
            }
        }
    });
    var geojson2MarkerOptions = {
            radius: 20,
            fillColor: "#ff7800",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.7
        };
    var geojson2Circle = L.geoJson(dataKabupaten, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, geojson2MarkerOptions);
        },
        filter: function(feature){
            if(beritaKabupaten.filter(k => k?.kabupaten.toLowerCase() == feature.properties.kabupaten.toLowerCase()).length > 0){
                return true
            }
        }
    });
    var markersKabupaten = new L.FeatureGroup();
    var markersKabupatenCircle = new L.FeatureGroup();
    markersKabupaten.addLayer(geojson2);
    markersKabupatenCircle.on('click', function(e) {
        map.flyTo(e.latlng, 11);
    })
    markersKabupatenCircle.addLayer(geojson2Circle);

    //provinsi
    var geojson = L.geoJson(dataProvinsi, {
        style: {
            opacity: 0,
            fillOpacity: 0
        },
        onEachFeature: onEachFeature
    }).addTo(map);

    var geojsonMarkerOptions = {
            radius: 20,
            fillColor: "#07C0FF",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.55
        };

    var geojsonCircle = L.geoJson(dataProvinsi, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, geojsonMarkerOptions);
        }
        // onEachFeature: onEachFeature
    }).addTo(map);

    var markersProvinsi = new L.FeatureGroup();
    var markersProvinsiCircle = new L.FeatureGroup();

    markersProvinsi.addLayer(geojson);
    markersProvinsiCircle.on('click', function(e) {
        map.flyTo(e.latlng, 8);
    })
    markersProvinsiCircle.addLayer(geojsonCircle);

    //mengatur zoom untuk menampilkan/menghilangkan marker
    map.on('zoomend', function(e) {
        var zoomLevel = map.getZoom();
        console.log(zoomLevel);
        if (zoomLevel > 5 && zoomLevel <= 7) { //untuk memunculkan marker provinsi, zoom 6
            map.addLayer(markersProvinsi);
            map.addLayer(geojsonCircle);
        } else {
            map.removeLayer(markersProvinsi);
            map.removeLayer(geojsonCircle);
            map.removeLayer(geojson2Circle);
        }
        if (zoomLevel > 7 && zoomLevel < 10) { //untuk memunculkan marker kabupaten, zoom 7-8
            map.addLayer(markersKabupaten);
            map.addLayer(geojson2Circle);
        } else {
            map.removeLayer(markersKabupaten);
            map.removeLayer(geojson2Circle);
        }
        if (zoomLevel >= 10) {
            map.addLayer(markersKecamatan);
            map.addLayer(geojson3Circle);

        } else {
            map.removeLayer(markersKecamatan);
            map.removeLayer(geojson3Circle);
        }
    });

    function onEachFeature3(feature, layer) {
        var kecamatan = beritaKecamatan.filter(k => k?.kecamatan.toLowerCase() == feature.properties.kecamatan.toLowerCase())[0];
        if(!kecamatan){
            return
        }
        let popUpText = 'Kecamatan : ' + feature.properties.kecamatan;
        if(kecamatan){
            if (kecamatan.kategori.bencana) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.bencana.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_t.png')}}">`
                }
                popUpText += (' <b>Bencana</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'bencana');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (kecamatan.kategori.kriminalitas) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.kriminalitas.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["Sedang", "Rendah"].includes(icon) && key == "Tinggi"){
                            icon = key;
                        }else if(icon == "Rendah" && key == "Sedang"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "Tinggi"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_p.png')}}">`
                } else if(icon == "Sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_s.png')}}">`
                }else if(icon =="Rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_t.png')}}">`
                }
                popUpText += (' <b>Kriminalitas</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'kriminalitas');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (kecamatan.kategori.kesehatan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.kesehatan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                        }
                    }
                    beritaText += (key + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_t.png')}}">`
                }
                popUpText += (' <b>Kesehatan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'kesehatan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kecamatan.kategori.ekonomi) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.ekonomi.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_t.png')}}">`
                }
                popUpText += (' <b>Ekonomi</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'ekonomi');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kecamatan.kategori.kecelakaan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.kecelakaan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_t.png')}}">`
                }
                popUpText += (' <b>Kecelakaan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'kecelakaan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kecamatan.kategori.olahraga) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kecamatan.kategori.olahraga.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["nasional", "provkota"].includes(icon) && key == "internasional"){
                            icon = key;
                        }else if(icon == "provkota" && key == "nasional"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "internasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_p.png')}}">`
                } else if(icon == "nasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_s.png')}}">`
                }else if(icon =="provkota"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_t.png')}}">`
                }
                popUpText += (' <b>Olahraga</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kecamatan');
                url.searchParams.append('daerah', kecamatan.kecamatan);
                url.searchParams.append('kategori', 'olahraga');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }
        }
        layer.bindPopup(popUpText);
    }

    // console.log(geojson3);
    // console.log(markersKecamatan);

    function onEachFeature2(feature, layer) {
        var kabupaten = beritaKabupaten.filter(k => k?.kabupaten.toLowerCase() == feature.properties.kabupaten.toLowerCase())[0];
        if(!kabupaten){
            return
        }
        let popUpText = 'Kabupaten : ' + feature.properties.kabupaten;
        if(kabupaten){
            if (kabupaten.kategori.bencana) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.bencana.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_t.png')}}">`
                }
                popUpText += (' <b>Bencana</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'bencana');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (kabupaten.kategori.kriminalitas) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.kriminalitas.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["Sedang", "Rendah"].includes(icon) && key == "Tinggi"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "Rendah" && key == "Sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "Tinggi"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_p.png')}}">`
                } else if(icon == "Sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_s.png')}}">`
                }else if(icon =="Rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_t.png')}}">`
                }
                popUpText += (' <b>Kriminalitas</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'kriminalitas');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (kabupaten.kategori.kesehatan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.kesehatan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) +  ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_t.png')}}">`
                }
                popUpText += (' <b>Kesehatan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'kesehatan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kabupaten.kategori.ekonomi) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.ekonomi.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_t.png')}}">`
                }
                popUpText += (' <b>Ekonomi</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'ekonomi');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kabupaten.kategori.kecelakaan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.kecelakaan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_t.png')}}">`
                }
                popUpText += (' <b>Kecelakaan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'kecelakaan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (kabupaten.kategori.olahraga) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(kabupaten.kategori.olahraga.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["nasional", "provkota"].includes(icon) && key == "internasional"){
                            icon = key;
                        }else if(icon == "provkota" && key == "nasional"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "internasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_p.png')}}">`
                } else if(icon == "nasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_s.png')}}">`
                }else if(icon =="provkota"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_t.png')}}">`
                }
                popUpText += (' <b>Olahraga</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'kabupaten');
                url.searchParams.append('daerah', kabupaten.kabupaten);
                url.searchParams.append('kategori', 'olahraga');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }
        }
        layer.bindPopup(popUpText);
    }

    function onEachFeature(feature, layer) {
        var provinsi = beritaProvinsi.filter(k => k?.provinsi.toLowerCase() == feature.properties.provinsi.toLowerCase())[0];
        let popUpText = 'Provinsi : ' + feature.properties.provinsi + "<br>" ;
        if(provinsi){
            if (provinsi.kategori.bencana) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.bencana.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/bencana_t.png')}}">`
                }
                popUpText += (' <b>Bencana</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'bencana');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (provinsi.kategori.kriminalitas) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.kriminalitas.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["Sedang", "Rendah"].includes(icon) && key == "Tinggi"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "Rendah" && key == "Sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "Tinggi"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_p.png')}}">`
                } else if(icon == "Sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_s.png')}}">`
                }else if(icon =="Rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kriminal_t.png')}}">`
                }
                popUpText += (' <b>Kriminalitas</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'kriminalitas');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)

            }if (provinsi.kategori.kesehatan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.kesehatan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kesehatan_t.png')}}">`
                }
                popUpText += (' <b>Kesehatan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'kesehatan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (provinsi.kategori.ekonomi) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.ekonomi.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/ekonomi_t.png')}}">`
                }
                popUpText += (' <b>Ekonomi</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'ekonomi');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (provinsi.kategori.kecelakaan) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.kecelakaan.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["sedang", "rendah"].includes(icon) && key == "parah"){
                            icon = key;
                            // console.log(key, iconValue);
                        }else if(icon == "rendah" && key == "sedang"){
                            icon = key;
                            // console.log(key, iconValue);
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "parah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_p.png')}}">`
                } else if(icon == "sedang"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_s.png')}}">`
                }else if(icon =="rendah"){
                    popUpText += `<br><br><img src="{{ asset('icons/kecelakaan_t.png')}}">`
                }
                popUpText += (' <b>Kecelakaan</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'kecelakaan');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }if (provinsi.kategori.olahraga) {
                let icon = "", iconValue = 0, beritaText = "";
                for(const [key, value] of Object.entries(provinsi.kategori.olahraga.keparahan)){
                    if(value > iconValue){
                        icon = key;
                        iconValue = value;
                    } else if(value == iconValue){
                        if(["nasional", "provkota"].includes(icon) && key == "internasional"){
                            icon = key;
                        }else if(icon == "provkota" && key == "nasional"){
                            icon = key;
                        }
                    }
                    beritaText += (key.charAt(0).toUpperCase() + key.slice(1) + ' : ' + value + ' berita<br>')
                }
                if(icon == "internasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_p.png')}}">`
                } else if(icon == "nasional"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_s.png')}}">`
                }else if(icon =="provkota"){
                    popUpText += `<br><br><img src="{{ asset('icons/olahraga_t.png')}}">`
                }
                popUpText += (' <b>Olahraga</b><br>')
                popUpText += beritaText
                let url = new URL('http://127.0.0.1:8000/tabel');
                url.searchParams.append('tipe', 'provinsi');
                url.searchParams.append('daerah', provinsi.provinsi);
                url.searchParams.append('kategori', 'olahraga');
                url.searchParams.append('source', filter_source);
                url.searchParams.append('range', filter_range);
                popUpText += (`<a href="${url.href}">Detail Berita</a><br>`)
            }
        }

        layer.bindPopup(popUpText);
    }

    map.attributionControl.addAttribution('Tingkat Keparahan &copy; Peta Kabar</a>');
</script>

</html>
