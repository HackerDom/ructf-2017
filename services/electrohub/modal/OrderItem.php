<?php

    require_once 'BaseModel.php';

    class OrderItem extends BaseModel
    {

        static $name_fields = [
            'id',
            'order_id',
            'position_x',
            'position_y',
            'quantity_energy'
        ];
        public static $table_name = 'order_item';

        public static function crate_model()
        {
            $query = 'CREATE TABLE IF NOT EXISTS ' . self::get_table_name() . '(';
            $query .= 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,';
            $query .= 'order_id INT NOT NULL,';
            $query .= 'position_x VARCHAR(1) NOT NULL,';
            $query .= 'position_y VARCHAR(1) NOT NULL,';
            $query .= 'quantity_energy INT NOT NULL';
            $query .= ')';
            return self::$db->query($query);
        }
    }

    $order_item = new OrderItem(
        [
            'order_id' => 1,
            'position_x' => 'x',
            'position_y' => 'y',
            'quantity_energy' => 100
        ]
    );
    $order_item->insert_or_update();