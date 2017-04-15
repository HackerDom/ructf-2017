<?php
    require_once 'BaseModel.php';

    class Order extends BaseModel
    {
        static $name_fields = [
            'id',
            'user_id',
            'name',
            'secret_code'
        ];
        public static $table_name = 'orders';


        public static function crate_model()
        {
            $query = 'CREATE TABLE IF NOT EXISTS ' . self::get_table_name() . '(';
            $query .= 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,';
            $query .= 'user_id INT NOT NULL,';
            $query .= 'name VARCHAR(255) NOT NULL,';
            $query .= 'secret_code VARCHAR(255) NOT NULL';
            $query .= ')';
            return self::query($query, true);
        }

        public static function get_all_by_user()
        {
            $query = 'SELECT * FROM ' . self::get_table_name() . ' WHERE user_id=' . $_SESSION['user_id'];
            $result = self::query($query);
            return Order::load_objects($result);
        }

    }
