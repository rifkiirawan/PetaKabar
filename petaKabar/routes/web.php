<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\KeywordController;
use App\Http\Controllers\PetaController;
use App\Http\Controllers\ScrapController;
use App\Http\Controllers\TabelController;


/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

// Route::get('/', function () {
//     return view('pane');
// });

// Route::get('/tabel', function () {
//     return view('tabel');
// });

// Route::get('/nopane', function () {
//     return view('nopane');
// });

Route::get('/', [PetaController::class, 'index']);
Route::post('/filterMap', [PetaController::class, 'filter'])->name('filterMap');
Route::get('/tabel', [TabelController::class, 'index']);
Route::post('/filterTable', [TabelController::class, 'filter'])->name('filterTable');
Route::get('/scrap', [ScrapController::class, 'index']);

Route::prefix('admin')->middleware('auth')->name('admin.')->group(function () {
    Route::prefix('keyword')->name('keyword.')->group(function () {
        Route::get('/', [KeywordController::class, 'index'])->name('index');
        Route::get('/create', [KeywordController::class, 'create'])->name('create');
        Route::post('/', [KeywordController::class, 'store'])->name('store');
        Route::get('/{id}/delete', [KeywordController::class, 'destroy'])->name('destroy');
    });
});

Auth::routes();
