<?php
//    require_once __DIR__ . '/core/DB.php';

    require_once __DIR__ . '/core/Router.php';
    require_once __DIR__ . '/core/Utils.php';
    require_once __DIR__ . '/modal/User.php';

    require_once __DIR__ . '/controllers/Index.php';
    require_once __DIR__ . '/controllers/Login.php';
    require_once __DIR__ . '/controllers/Signup.php';
    require_once __DIR__ . '/controllers/Signout.php';


    $r = new Router();

    $r->add_route('/index/', new Index());
    $r->add_route('/signin/', new Login());
    $r->add_route('/signup/', new Signup());
    $r->add_route('/signout/', new Signout());

    $controller = $r->find($_SERVER['REQUEST_URI']);

    if ($controller) {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            echo $controller->post();
        } else if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            echo $controller->get();
        } else {
            error(404);
        }
    } else {
        error(404);
    }

