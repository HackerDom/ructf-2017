<?php

    class Session
    {
        public static function init()
        {
            session_start();
            if (!array_key_exists('auth', $_SESSION))
                $_SESSION['auth'] = false;
        }

        public static function is_authenticated()
        {
            return $_SESSION['auth'];
        }


        public static function login(string $login, string $password)
        {
            $result = User::check_login_and_password($login, $password);
            if ($result && !$_SESSION['auth']) {
                $_SESSION['auth'] = true;
                $_SESSION['login'] = $result->login;
                $_SESSION['user_id'] = $result->id;
                return true;
            }
            return false;
        }

        public static function logout()
        {
            $_SESSION['auth'] = false;
            unset($_SESSION['login']);
            unset($_SESSION['user_id']);
        }
    }

    Session::init();