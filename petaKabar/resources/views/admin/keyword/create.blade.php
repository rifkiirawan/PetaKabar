@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">{{ __('Tambah Keyword') }}</div>

                <div class="card-body">
                    <div class="my-3">
                        <a href="{{route('admin.keyword.index')}}" class="btn btn-secondary">Kembali</a>
                    </div>
                    <form action="{{route('admin.keyword.store')}}" method="POST">
                        {{ csrf_field() }}
                        <div class="form-group my-3">
                            <label for="nama_keyword">Keyword</label>
                            <input required type="text" class="form-control" id="nama_keyword" name="nama_keyword" autocomplete="off">
                            <div id="nama_keywordhelp" class="form-text">*Untuk situs berita Tribunnews hanya dapat menggunakan 1 kata.</div>
                        </div>
                        <div class="form-group my-3">
                            <label for="source">Sumber</label>
                            <select class="form-select" name="source">
                                <option value="detik">Detik</option>
                                <option value="tribun">Tribunnews</option>
                                <option value="kompas">Kompas</option>
                                <option value="tempo">Tempo</option>
                            </select>
                        </div>
                        <div class="form-group my-3">
                            <label for="topik_id">Topik</label>
                            <select class="form-select" name="topik_id">
                                @foreach ($topik as $tp)
                                    <option value="{{$tp->ID}}">{{$tp->nama_topik}}</option>
                                @endforeach
                            </select>
                        </div>

                        <button type="submit" class="btn btn-primary" style="margin-top:10px">Simpan</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
