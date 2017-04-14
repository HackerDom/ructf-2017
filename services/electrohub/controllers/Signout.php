<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';

    class Signout extends Controller
    {
        function post()
        {
            Session::logout();
            redirect('/signin/');
        }

        function get()
        {

            Session::logout();
            redirect('/signin/');
        }
    }