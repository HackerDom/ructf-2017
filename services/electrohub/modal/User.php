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
            $query .= 'giro VARCHAR(255) NOT NULL';
            $query .= ')';
            return self::query($query, $create = true);
        }



        protected function update()
        {
            $query = "UPDATE " . self::get_table_name() . " SET ";
            $query .= "login=" . self::$db->escape_value($this->login) . ", ";
            $query .= "first_name=" . self::$db->escape_value($this->first_name) . ", ";
            $query .= "last_name=" . self::$db->escape_value($this->last_name) . ", ";
            $query .= "password=" . self::$db->escape_value($this->password) . ", ";
            $query .= "giro=" . self::$db->escape_value($this->giro);
            $query .= " WHERE id=$this->id";
            return self::query($query);
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

