<?php


    require_once 'BaseModel.php';

    class User extends BaseModel
    {
        public static $name_fields = [
            'id',
            'login',
            'first_name',
            'last_name',
            'password',
            'privet_type',
            'giro'
        ];
        public static $table_name = 'users';


        public static function crate_model()
        {
            $query = 'CREATE TABLE IF NOT EXISTS ' . self::get_table_name() . '(';
            $query .= 'id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,';
            $query .= 'login VARCHAR(255) NOT NULL,';
            $query .= 'first_name VARCHAR(255) NOT NULL,';
            $query .= 'last_name VARCHAR(255) NOT NULL,';
            $query .= 'password VARCHAR(255) NOT NULL,';
            $query .= 'privet_type BOOLEAN NOT NULL default 0,';
            $query .= 'giro VARCHAR(255) NOT NULL';
            $query .= ')';
            return self::query($query, $create = true);
        }


        public static function get_by_login(string $login)
        {
            $query = "SELECT * FROM " . self::get_table_name() . " WHERE login=" . self::$db->escape_value($login);
            return self::query($query)->fetch_assoc();
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

