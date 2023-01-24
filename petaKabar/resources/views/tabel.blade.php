@extends('layouts.master', ['title'=>''])

@section('content-header')
<div class="container-fluid">
    <div class="row mb-2">
        <div class="col-sm-6">
            <h1 class="m-0">Peta Kabar</h1>
        </div><!-- /.col -->
        <!-- <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item active">Peta Kabar</li>
            </ol>
        </div>/.col -->
    </div><!-- /.row -->
</div><!-- /.container-fluid -->
@endsection

@section('content')
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Detail Berita Peta Kabar</h3>
                    <!-- <div class="float-right">
                        <a class="btn btn-success" href="/">Buka Peta!</a>
                    </div> -->
                </div>
                <!-- /.card-header -->
                <div class="card-body">
                    <div class="row mb-5">
                        <div class="col-12">
                            <form action="{{route('filterTable')}}" method="POST">
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
                                <button type="submit" class="btn btn-primary">Filter Berita</button>
                            </form>
                        </div>
                    </div>

                    <table id="example1" class="table table-bordered table-hover table-responsive">
                        <thead>
                            <tr>
                                <th>Kategori</th><!-- column 2 -->
                                <th>Judul</th>
                                <!-- <th>Kesimpulan</th>  -->
                                <th>Kejadian</th> <!-- column 34567 -->
                                <th>Waktu Berita</th>
                                <th>Sumber Berita</th>
                                <th>Orang Terlibat</th>
                                <th>Provinsi</th> <!-- column 891011 -->
                                <th>Kabupaten</th>
                                <th>Kecamatan</th>
                                <th>Tingkat Keparahan</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($data as $respons)
                            <tr style="text-transform: capitalize">
                                <td>{{$respons['kategori']}}</td>
                                <td>{{$respons['title']}}</td>
                                <!-- <td>{{$respons['summary']}}</td> -->
                                <td>{{$respons['nama_kejadian']}}</td>
                                <td>{{$respons['waktu']}}</td>
                                <td>{{$respons['sumber']}}</td>
                                <td>{{$respons['orang_terlibat']}}</td>
                                <td>{{$respons['provinsi']}}</td>
                                <td>{{$respons['kabupaten']}}</td>
                                <td>{{$respons['kecamatan']}}</td>
                                <td>{{$respons['tingkat_keparahan']}}</td>
                            </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
                <!-- /.card-body -->
            </div>
        </div>
    </div>
</div>
<!-- /.container-fluid -->
@endsection

<!-- JS tertentu jika ingin beda dari page yang lain -->
@push('js')
<script>
    $(function() {
        $('#example1 thead tr')
            .clone(true)
            .addClass('filters')
            .appendTo('#example1 thead');

        $("#example1").DataTable({
            "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Indonesian.json"
            },
            "lengthChange": false,
            "autoWidth": false,
            // "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"],
            "orderCellsTop": true,
            "fixedHeader": true,
            "initComplete": function () {
                var api = this.api();

                // For each column
                api
                    .columns()
                    .eq(0)
                    .each(function (colIdx) {
                        // Set the header cell to contain the input element
                        var cell = $('.filters th').eq(
                            $(api.column(colIdx).header()).index()
                        );
                        var title = $(cell).text();
                        $(cell).html('<input type="text" placeholder="' + title + '" />');

                        // On every keypress in this input
                        $(
                            'input',
                            $('.filters th').eq($(api.column(colIdx).header()).index())
                        )
                            .off('keyup change')
                            .on('change', function (e) {
                                // Get the search value
                                $(this).attr('title', $(this).val());
                                var regexr = '({search})'; //$(this).parents('th').find('select').val();

                                var cursorPosition = this.selectionStart;
                                // Search the column for that value
                                api
                                    .column(colIdx)
                                    .search(
                                        this.value != ''
                                            ? regexr.replace('{search}', '(((' + this.value + ')))')
                                            : '',
                                        this.value != '',
                                        this.value == ''
                                    )
                                    .draw();
                            })
                            .on('keyup', function (e) {
                                e.stopPropagation();

                                $(this).trigger('change');
                                $(this)
                                    .focus()[0]
                                    .setSelectionRange(cursorPosition, cursorPosition);
                            });
                    });
            },
        }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');

        $('#example2').DataTable({
            "paging": true,
            "lengthChange": false,
            "searching": false,
            "ordering": true,
            "info": true,
            "autoWidth": false,
            "responsive": true,
        });
    });
</script>


@endpush
