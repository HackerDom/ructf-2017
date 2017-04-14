<?php


    class Company extends BaseModel
    {
        static $db;
        private $name_fields = [
            'id',
            'user_id',
            ''
        ];
        public static $table_name = 'application';
    }

    User::$db = new DB();