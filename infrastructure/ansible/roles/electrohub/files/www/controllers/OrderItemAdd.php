<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/Order.php';
    require_once __DIR__ . '/../modal/OrderItem.php';

    class OrderItemAdd extends Controller
    {
        public $template = 'order_item_add.twig';

        function post()
        {
            if (Session::is_authenticated()) {
                $order = Order::get_by_id($this->option['order_id']);
                if ($order && $order['user_id'] === $_SESSION['user_id']) {
                    $order_item = new OrderItem([
                        'order_id' => $this->option['order_id'],
                        'position_x' => $_POST['position_x'],
                        'position_y' => $_POST['position_y'],
                        'quantity_energy' => $_POST['quantity_energy']
                    ]);
                    $order_item->insert_or_update();
                    redirect('/order/' . $this->option['order_id'] . '/');
                } else {
                    redirect('/order/add/');
                }
            } else {
                redirect('/signin/');
            }
        }

        function get()
        {
            if (Session::is_authenticated()) {
                $order = Order::get_by_id($this->option['order_id']);
                if ($order && $order['user_id'] === $_SESSION['user_id']) {
                    echo parent::render();
                } else {
                    redirect('/order/add/');
                }
            } else {
                redirect('/signin/');
            }
        }
    }