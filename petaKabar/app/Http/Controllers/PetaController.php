<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

use Carbon\Carbon;

class PetaController extends Controller
{
    public function index(Request $request)
    {
        // $response = Http::accept('application/json')->get('http://jsonblob.com/api/1039541677303545856');
        // $response = $response->json()["data"];
        $check = null;
        $message = null;

        $source = "all";
        $range = "week";
        $topic = "all";

        $currTime = Carbon::now()->toDateTimeString();
        $requestedTime = Carbon::now();
        $response = [];
        $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                    ->get();

        foreach($query as $q) {
            $nama_kejadian = "[";
            $kejadian = explode(", ", $q->nama_kejadian);
            for($i = 0; $i < count($kejadian); $i++) {
                $nama_kejadian = $nama_kejadian . "'". $kejadian[$i];
                if($i < count($kejadian) - 1) {
                    $nama_kejadian = $nama_kejadian . "', ";
                }
                else {
                    $nama_kejadian = $nama_kejadian . "'";
                }
            }
            $nama_kejadian = $nama_kejadian . "]";

            $orang_terlibat = "[";
            $terlibat = explode(", ", $q->orang_terlibat);
            for($i = 0; $i < count($terlibat); $i++) {
                $orang_terlibat = $orang_terlibat . "'". $terlibat[$i];
                if($i < count($terlibat) - 1) {
                    $orang_terlibat = $orang_terlibat . "', ";
                }
                else {
                    $orang_terlibat = $orang_terlibat . "'";
                }
            }
            $orang_terlibat = $orang_terlibat . "]";
            $kategorilow = strtolower($q->kategori);
            $arr = array(
                        'title' => $q->title,
                        'kategori' => $kategorilow,
                        'nama_kejadian' => $nama_kejadian,
                        'waktu' => $q->waktu,
                        'orang_terlibat' => $orang_terlibat,
                        'provinsi' => $q->provinsi,
                        'kabupaten' => $q->kabupaten,
                        'kecamatan' => $q->kecamatan,
                        'tingkat_keparahan' => $q->tingkat_keparahan,
                    );

            array_push($response, $arr);
        }

        return view('nopane', compact('response', 'check', 'message', 'source', 'range', 'topic'));
    }

    public function filter(Request $request)
    {
        $this->validate($request, [
            'source' => 'required',
            'range' => 'required',
            'topic' => 'required',
        ]);

        $check = null;
        $message = null;

        $source = $request->source;
        $range = $request->range;
        $topic = $request->topic;

        $currTime = Carbon::now()->toDateTimeString();
        $requestedTime = Carbon::now();
        $response = [];

        if(($request->source == "all") && ($request->topic == "all") ) { #sumber semua, topik semua
            if($request->range == "all") { #tanggal semua
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->get();
            }
            else if($request->range == "year") { #tanggal tahun
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($request->range == "month") { #tanggal bulan
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($request->range == "week") { #tanggal minggu
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($request->range == "day") { #tanggal hari
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                ->get();
            }
        }
        else if (($request->source == "all") && ($request->topic != "all")) { #sumber semua, topik gak semua
            if($request->range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->get();
            }
            else if($request->range == "year") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "month") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "week") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "day") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                    ->get();
            }
        }
        else if (($request->source != "all") && ($request->topic == "all")){
            if($request->range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->get();
                    
            }
            else if($request->range == "year") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "month") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "week") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "day") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                    ->get();
            }
        }
        else { #topik not all, sumber not all
            if($request->range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->get();
                    
            }
            else if($request->range == "year") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "month") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "week") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($request->range == "day") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                    )
                    ->where('b.berita_source', 'like', $request->source)
                    ->where('b.berita_topik_id','=',$request->topic)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                    ->get();
            }
        }

        foreach($query as $q) {
            $nama_kejadian = "[";
            $kejadian = explode(", ", $q->nama_kejadian);
            for($i = 0; $i < count($kejadian); $i++) {
                $nama_kejadian = $nama_kejadian . "'". $kejadian[$i];
                if($i < count($kejadian) - 1) {
                    $nama_kejadian = $nama_kejadian . "', ";
                }
                else {
                    $nama_kejadian = $nama_kejadian . "'";
                }
            }
            $nama_kejadian = $nama_kejadian . "]";

            $orang_terlibat = "[";
            $terlibat = explode(", ", $q->orang_terlibat);
            for($i = 0; $i < count($terlibat); $i++) {
                $orang_terlibat = $orang_terlibat . "'". $terlibat[$i];
                if($i < count($terlibat) - 1) {
                    $orang_terlibat = $orang_terlibat . "', ";
                }
                else {
                    $orang_terlibat = $orang_terlibat . "'";
                }
            }
            $orang_terlibat = $orang_terlibat . "]";
            $kategorilow = strtolower($q->kategori);
            $arr = array(
                        'title' => $q->title,
                        'kategori' => $kategorilow,
                        'nama_kejadian' => $nama_kejadian,
                        'waktu' => $q->waktu,
                        'orang_terlibat' => $orang_terlibat,
                        'provinsi' => $q->provinsi,
                        'kabupaten' => $q->kabupaten,
                        'kecamatan' => $q->kecamatan,
                        'tingkat_keparahan' => $q->tingkat_keparahan,
                    );

            array_push($response, $arr);
        }

        return view('nopane', compact('response', 'check', 'message', 'source', 'range','topic'));
    }
}
