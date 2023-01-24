<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

use Carbon\Carbon;


class ScrapController extends Controller
{
    public function index(Request $request)
    {
        // exec('py D:\sem9\program\TA_petakabar\tes.py', $output, $returnvar);
        exec('py D:\sem9\program\TA_petakabar\main.py', $output, $returnvar);
        exec('py D:\sem9\TA_petakabar\main.py', $output, $returnvar);
        $check = 1;
        // dd($output[0]);
        #gagal menjalankan program
        if($output[0] != "success") {
            $message = "Proses scrapping gagal dijalankan.";
        }
        #berhasil menjalankan program
        else {
            $check = 2;
            $message = "Proses scrapping berhasil dijalankan.";
        }
        // dd($output, $returnvar, $message);

        $source = "all";
        $range = "week";
        $topic = "all";

        // $response = Http::accept('application/json')->get('http://jsonblob.com/api/1039541677303545856');
        // $response = $response->json()["data"];

        $response = [];
        $currTime = Carbon::now()->toDateTimeString();
        $requestedTime = Carbon::now();

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
}
