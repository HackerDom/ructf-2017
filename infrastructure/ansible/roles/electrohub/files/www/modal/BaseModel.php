<?php
    require_once __DIR__ . '/../core/DB.php';

    class BaseModel
    {
        static $db;

        function __construct(array $fields = [])
        {
            if (!$this->is_exists_table()) {
                $this->crate_model();
            }
            foreach ($fields as $name_field => $value_field) {
                $this->$name_field = $value_field;
            }
            foreach (self::get_name_fields() as $name_field) {
                if (!isset($this->$name_field)) {
                    $this->$name_field = NULL;
                }
            }

        }

        public static function load_objects($result)
        {
            $objects = [];
            $class = get_called_class();
            while ($order_object = $result->fetch_assoc()) {
                $objects[] = new $class($order_object);
            }
            return $objects;
        }

        public static function get_name_fields()
        {
            $class = get_called_class();
            return $class::$name_fields;
        }

        public static function get_table_name()
        {
            $class = get_called_class();
            return $class::$table_name;
        }

        protected function insert()
        {
            $query = "INSERT INTO " . self::get_table_name() . " SET ";
            $set_field = [];
            foreach (self::get_name_fields() as $name_field) {
                if ($name_field != 'id') {
                    $set_field[] = $name_field . "=" . self::$db->escape_value($this->$name_field);
                }
            }
            $query .= join(', ', $set_field);
            return self::query($query);
        }

        protected function update()
        {
            $query = "UPDATE " . self::get_table_name() . " SET ";
            $set_field = [];
            foreach (self::get_name_fields() as $name_field) {
                if ($name_field != 'id') {
                    $set_field[] = $name_field . "=" . self::$db->escape_value($this->$name_field);
                }
            }
            $query .= join(', ', $set_field);
            $query .= " WHERE id=" . $this->id;
            return self::query($query);
        }

        public static function crate_model()
        {
            $class = get_called_class();
            return $class::crate_model();
        }

        protected static function query(string $query, bool $create = false)
        {

            if (!self::is_exists_table() and !$create) {
                self::crate_model();
            }
            return self::$db->query($query);
        }

        public function insert_or_update()
        {
            self::$db->connect->begin_transaction();
            if (isset($this->id)) {
                $result = $this->update($this->id);
            } else {
                $result = $this->insert();
                if ($result) {
                    $this->id = self::$db->connect->insert_id;
                }
            }
            self::$db->connect->commit();
            return $result;
        }


        protected static function is_exists_table()
        {
            $query = "SHOW TABLES LIKE '" . self::get_table_name() . "'";
            return self::$db->query($query)->num_rows;
        }


        public static function get_by_id(int $id)
        {
            $query = "SELECT * FROM " . self::get_table_name() . " WHERE id=$id";
            return self::$db->query($query)->fetch_assoc();
        }

    }

    BaseModel::$db = new DB();