<?php

    require_once __DIR__ . '/../core/DB.php';

    class User
    {
        static $db;
        private $name_fields = [
            'id', 'login', 'first_name', 'last_name', 'password', 'giro'
        ];
        private static $table_name = 'users';


        function __construct(array $fields = [])
        {
            if (!$this->is_exists_table()) {
                $this->crate_model();
            }
            foreach ($fields as $name_field => $value_field) {
                $this->$name_field = $value_field;
            }
            foreach ($this->name_fields as $name_field) {
                if (!isset($this->$name_field)) {
                    $this->$name_field = '';
                }
            }

        }

        private function is_exists_table()
        {
            $query = "SHOW TABLES LIKE '" . self::$table_name . "'";
            return self::$db->query($query)->num_rows;
        }

        private function crate_model()
        {
            $query = 'CREATE TABLE IF NOT EXISTS ' . self::$table_name . '(';
            $query .= 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,';
            $query .= 'login VARCHAR(255) NOT NULL,';
            $query .= 'first_name VARCHAR(255) NOT NULL,';
            $query .= 'last_name VARCHAR(255) NOT NULL,';
            $query .= 'password VARCHAR(255) NOT NULL,';
            $query .= 'giro VARCHAR(255) NOT NULL';
            $query .= ')';
            return self::$db->query($query);
        }

        public function insert()
        {
            $this->password = password_hash($this->password, PASSWORD_BCRYPT);
            $query = "INSERT INTO " . self::$table_name . " SET ";
            $query .= "login=" . self::$db->escape_value($this->login) . ", ";
            $query .= "first_name=" . self::$db->escape_value($this->first_name) . ", ";
            $query .= "last_name=" . self::$db->escape_value($this->last_name) . ", ";
            $query .= "password=" . self::$db->escape_value($this->password) . ", ";
            $query .= "giro=" . self::$db->escape_value($this->giro);
            return self::$db->query($query);
        }

        public function update(int $id)
        {
            $query = "UPDATE " . self::$table_name . " SET ";
            $query .= "login=" . self::$db->escape_value($this->login) . ", ";
            $query .= "first_name=" . self::$db->escape_value($this->first_name) . ", ";
            $query .= "last_name=" . self::$db->escape_value($this->last_name) . ", ";
            $query .= "password=" . self::$db->escape_value($this->password) . ", ";
            $query .= "giro=" . self::$db->escape_value($this->giro);
            $query .= " WHERE id=$id";
            return self::$db->query($query);
        }

        public static function get_by_id(int $id)
        {
            $query = "SELECT * FROM " . self::$table_name . " WHERE id=$id";
            return self::$db->query($query)->fetch_assoc();
        }


        public static function get_by_login(string $login)
        {
            $query = "SELECT * FROM " . self::$table_name . " WHERE login=" . self::$db->escape_value($login);
            return self::$db->query($query)->fetch_assoc();
        }


        public static function check_login_and_password($login, $password)
        {

            $user = new User(User::get_by_login($login));

            if (password_verify($password, $user->password)) {
                return $user;
            } else {
                return false;
            }
        }
    }
//
    User::$db = new DB();
//    $user = new User([
//        'login' => 'login',
//        'first_name' => 'first_name',
//        'last_name' => 'last_name',
//        'password' => 'password',
//        'giro' => 'giro'
//    ]);
//
////    $user->insert();
////    $user->last_name = 'last_name2';
////    $user->update(1);
////
//    echo var_dump(User::check_login_and_password('login', 'password'));
//
//    echo var_dump(User::check_login_and_password('login', 'password2'));