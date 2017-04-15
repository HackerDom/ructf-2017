<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/Order.php';

    class OrderAdd extends Controller
    {
        public $template = 'order_add.twig';

        function post()
        {
            if (Session::is_authenticated()) {
                $order = new Order([
                    'name' => $_POST['name'],
                    'secret_code' => $_POST['secret_code'],
                    'user_id' => $_SESSION['user_id'],
                ]);
                $order->insert_or_update();

            } else {
                redirect('/signin/');
            }
        }

        function get()
        {
            if (Session::is_authenticated()) {
                echo parent::render();
            } else {
                redirect('/signin/');
            }
        }
    }