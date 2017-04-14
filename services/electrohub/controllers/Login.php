<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';

    class Login extends Controller
    {
        public $template = 'signin.twig';

        function post()
        {
            $login = $_POST['login'];
            $password = $_POST['password'];
            Session::login($login, $password);
            if (!Session::is_authenticated()) {
                redirect('/signin/');
            } else {
                redirect('/index/');
            }
        }

        function get()
        {
            if (Session::is_authenticated()) {
                redirect('/index/');
            } else {
                echo parent::render();
            }
        }
    }