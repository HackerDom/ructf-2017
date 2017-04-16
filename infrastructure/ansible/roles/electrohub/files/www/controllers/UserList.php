<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/User.php';

    class UserList extends Controller
    {
        public $template = 'user_list.twig';


        function get()
        {
            $user_list = User::get_all();
            foreach ($user_list as $user) {
                $check_user = $_SESSION['user_id'] && $user->id === $_SESSION['user_id'];
                $half_len = intval(strlen($user->giro) / 2);
                $user->print_giro = !$user->private_type ? $user->giro : $check_user ? substr($user->giro, $half_len) : substr($user->giro, -$half_len);
            }

            echo parent::render(
                ['user_list' => $user_list]
            );

        }
    }