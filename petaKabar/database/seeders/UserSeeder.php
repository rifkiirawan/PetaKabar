<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::connection('mysql')
            ->table('users')
            ->insert([
                'name'	    => 'Admin',
                'email'	    => 'admin@gmail.com',
                'password'	=> Hash::make('password'),
            ]);
    }
}
