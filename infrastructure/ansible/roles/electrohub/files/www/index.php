<?php
//    require_once __DIR__ . '/core/DB.php';

    require_once __DIR__ . '/core/Router.php';
    require_once __DIR__ . '/core/Utils.php';
    require_once __DIR__ . '/modal/User.php';

    require_once __DIR__ . '/controllers/Index.php';
    require_once __DIR__ . '/controllers/Login.php';
    require_once __DIR__ . '/controllers/Signup.php';
    require_once __DIR__ . '/controllers/Signout.php';
    require_once __DIR__ . '/controllers/OrderAdd.php';
    require_once __DIR__ . '/controllers/OrderItemAdd.php';
    require_once __DIR__ . '/controllers/OrderList.php';
    require_once __DIR__ . '/controllers/OrderDetail.php';
    $route = new Router();

    $route->add_route('/index/', Index);
    $route->add_route('/order/add/', OrderAdd);
    $route->add_route('/order/:order_id/', OrderDetail);
    $route->add_route('/order/:order_id/add_item/', OrderItemAdd);
    $route->add_route('/order/', OrderList);
    $route->add_route('/signin/', Login);
    $route->add_route('/signup/', Signup);
    $route->add_route('/signout/', Signout);

    $controller = $route->find($_SERVER['REQUEST_URI']);

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

