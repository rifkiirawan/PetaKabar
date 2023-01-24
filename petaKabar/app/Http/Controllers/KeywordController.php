<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class KeywordController extends Controller
{
    public function index()
    {
        $keyword = DB::connection('mysql2')
            ->table('keyword as k')
            ->join('topik as t', 'k.topik_id', '=', 't.ID')
            ->select(
                'k.id as id',
                'k.nama_keyword as nama_keyword',
                'k.source as source',
                't.nama_topik as topik',
            )
            ->get();
        return view('admin.keyword.index', compact('keyword'));
    }

    public function create()
    {
        $topik = DB::connection('mysql2')
            ->table('topik')
            ->get();
        return view('admin.keyword.create', compact('topik'));
    }

    public function store(Request $request)
    {
        $this->validate($request, [
            'nama_keyword' => 'required',
            'source' => 'required',
            'topik_id' => 'required',
        ]);

        if($request->source == "tribun") {
            $keyword = explode(" ", $request->nama_keyword);
            if(count($keyword) > 1) {
                $message = ["fail" => "Untuk situs berita Tribunnews hanya boleh memasukkan 1 kata."];
                return redirect()->route('admin.keyword.index')->with($message);
            }
        }

        try {
            $keyword = DB::connection('mysql2')
                ->table('keyword')
                ->insert([
                    'nama_keyword' => $request->nama_keyword,
                    'source' => $request->source,
                    'topik_id' => $request->topik_id,
                ]);
            $message = ["success" => "Keyword berhasil di tambahkan!"];

        } catch (\Throwable $th) {
            $message = ["fail" => $th->getMessage()];
        }

        return redirect()->route('admin.keyword.index')->with($message);
    }

    public function destroy($id)
    {
        try{
            DB::connection('mysql2')
                ->table('keyword')
                ->where('ID', $id)
                ->delete();
            $message = ["success" => "Keyword berhasil di hapus!"];
        }catch(\Throwable $th){
            $message = ["fail" => $th->getMessage()];
        }
        return redirect()->route('admin.keyword.index')->with($message);
    }
}
