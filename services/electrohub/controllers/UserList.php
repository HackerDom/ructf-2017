<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/User.php';

    class OrderList extends Controller
    {
        public $template = 'user_list.twig';


        function get()
        {
            $user_list = User::get_all();
            foreach ($user_list as $user) {
                $check_user = $_SESSION['user_id'] && $user->id === $_SESSION['user_id'];
                $user->print_giro = !$user->privet_type ? $user->giro : $check_user ? $user->giro : 'privet';
            }
            echo parent::render(
                ['user_list' => User::get_all()]
            );

        }
    }