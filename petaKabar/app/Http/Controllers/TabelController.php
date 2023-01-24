<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

use Carbon\Carbon;

class TabelController extends Controller
{
    public function index(Request $request)
    {
        $tipe_daerah = ['kabupaten', 'kecamatan', 'provinsi'];
        $tipe = $request->query('tipe');
        $daerah = $request->query('daerah');
        $kategori = $request->query('kategori');

        $source = "all";
        $range = "all";
        if ($request->query('source')) {
            if ($request->query('source') == "kompas") {
                $source = "www.kompas.com";
            }
            else if ($request->query('source') == "tribun") {
                $source = "www.tribunnews.com";
            }
            else if ($request->query('source') == "tempo") {
                $source = "www.tempo.co";
            }
            else if ($request->query('source') == "detik") {
                $source = "www.detik.com";
            }
        }
        if ($request->query('range')) {
            $range = $request->query('range');
        }

        $currTime = Carbon::now()->toDateTimeString();
        $requestedTime = Carbon::now();

        // $response = Http::accept('application/json')->get('http://jsonblob.com/api/1039541677303545856');
        // $response = $response->json()["data"];

        $response = [];
        if($source == "all") {
            if($range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->get();
            }
            else if($range == "year") {
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($range == "month") {
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($range == "week") {
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                ->get();
            }
            else if($range == "day") {
                $query = DB::connection('mysql2')
                ->table('berita as b')
                ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                ->select(
                    'b.berita_title as title',
                    't.nama_topik as kategori',
                    'b.qe_what as nama_kejadian',
                    'b.ner_when as waktu',
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                ->get();
            }
        }
        else {
            if($range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $source)
                    ->get();
            }
            else if($range == "year") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subYear()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($range == "month") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subMonth()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($range == "week") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $source)
                    ->whereBetween('b.berita_qdate', [$requestedTime->subWeek()->toDateTimeString(), $currTime])
                    ->get();
            }
            else if($range == "day") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $source)
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

            $arr = array(
                        'title' => $q->title,
                        'kategori' => $q->kategori,
                        'nama_kejadian' => $nama_kejadian,
                        'waktu' => $q->waktu,
                        'sumber' => $q->sumber,
                        'orang_terlibat' => $orang_terlibat,
                        'provinsi' => $q->provinsi,
                        'kabupaten' => $q->kabupaten,
                        'kecamatan' => $q->kecamatan,
                        'tingkat_keparahan' => $q->tingkat_keparahan,
                        'summary' => $q->summary
                    );

            array_push($response, $arr);
        }

        $data = [];
        if ($tipe != 'all' && in_array($tipe, $tipe_daerah)) {
            for ($i=0; $i < count($response); $i++) {
                if(strtolower($response[$i][$tipe]) == strtolower($daerah) && strtolower($response[$i]['kategori']) == strtolower($kategori)){
                    array_push($data, $response[$i]);
                }
            }
        } elseif ($tipe == ''){
            $data = $response;
        }

        return view('tabel', compact('data', 'source', 'range'));
    }

    public function filter(Request $request)
    {
        $this->validate($request, [
            'source' => 'required',
            'range' => 'required',
        ]);

        $tipe_daerah = ['kabupaten', 'kecamatan', 'provinsi'];
        $tipe = $request->query('tipe');
        $daerah = $request->query('daerah');
        $kategori = $request->query('kategori');

        $source = $request->source;
        $range = $request->range;

        $currTime = Carbon::now()->toDateTimeString();
        $requestedTime = Carbon::now();
        $response = [];

        if($request->source == "all") {
            if($request->range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
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
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
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
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
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
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
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
                    'b.berita_source as sumber',
                    'b.ner_who as orang_terlibat',
                    'b.ner_prov as provinsi',
                    'b.ner_kab as kabupaten',
                    'b.ner_kec as kecamatan',
                    'b.class_classification as tingkat_keparahan',
                    'b.berita_summary as summary',
                )
                ->whereBetween('b.berita_qdate', [$requestedTime->subDay()->toDateTimeString(), $currTime])
                ->get();
            }
        }
        else {
            if($request->range == "all") {
                $query = DB::connection('mysql2')
                    ->table('berita as b')
                    ->join('topik as t', 'b.berita_topik_id', '=', 't.ID')
                    ->select(
                        'b.berita_title as title',
                        't.nama_topik as kategori',
                        'b.qe_what as nama_kejadian',
                        'b.ner_when as waktu',
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
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
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
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
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
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
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
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
                        'b.berita_source as sumber',
                        'b.ner_who as orang_terlibat',
                        'b.ner_prov as provinsi',
                        'b.ner_kab as kabupaten',
                        'b.ner_kec as kecamatan',
                        'b.class_classification as tingkat_keparahan',
                        'b.berita_summary as summary',
                    )
                    ->where('b.berita_source', 'like', $request->source)
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

            $arr = array(
                        'title' => $q->title,
                        'kategori' => $q->kategori,
                        'nama_kejadian' => $nama_kejadian,
                        'waktu' => $q->waktu,
                        'sumber' => $q->sumber,
                        'orang_terlibat' => $orang_terlibat,
                        'provinsi' => $q->provinsi,
                        'kabupaten' => $q->kabupaten,
                        'kecamatan' => $q->kecamatan,
                        'tingkat_keparahan' => $q->tingkat_keparahan,
                        'summary' => $q->summary
                    );

            array_push($response, $arr);
        }

        $data = [];
        if ($tipe != 'all' && in_array($tipe, $tipe_daerah)) {
            for ($i=0; $i < count($response); $i++) {
                if(strtolower($response[$i][$tipe]) == strtolower($daerah) && strtolower($response[$i]['kategori']) == strtolower($kategori)){
                    array_push($data, $response[$i]);
                }
            }
        } elseif ($tipe == ''){
            $data = $response;
        }

        return view('tabel', compact('data', 'source', 'range'));
    }
}
