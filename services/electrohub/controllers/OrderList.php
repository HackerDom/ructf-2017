<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/Order.php';

    class OrderList extends Controller
    {
        public $template = 'order_list.twig';


        function get()
        {
            if (Session::is_authenticated()) {
                echo parent::render(
                    [
                        'order_list' => Order::get_all_by_user()
                    ]
                );
            } else {
                redirect('/signin/');
            }
        }
    }