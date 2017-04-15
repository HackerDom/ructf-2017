<?php
    require_once __DIR__ . '/../core/Controller.php';
    require_once __DIR__ . '/../core/Session.php';
    require_once __DIR__ . '/../core/Utils.php';
    require_once __DIR__ . '/../modal/Order.php';
    require_once __DIR__ . '/../modal/OrderItem.php';

    class OrderDetail extends Controller
    {
        public $template = 'order_detail.twig';


        function get()
        {
            if (Session::is_authenticated()) {
                try {

                    $order = Order::get_by_id($this->option['order_id']);
                    $order_obj = new Order($order);

                    if ($order_obj->id && $order_obj->user_id == $_SESSION['user_id']) {
                        $query = 'SELECT * FROM ' . OrderItem::get_table_name() . ' where order_id=' . $this->option['order_id'];
                        $order_item_result = OrderItem::$db->query($query);
                        $order_item_list = [];
                        $hash = '';
                        if ($order_item_result) {
                            $order_item_list = OrderItem::load_objects($order_item_result);
                            foreach ($order_item_list as $order_item) {
                                $hash .= $order_item->position_x . $order_item->position_y;
                            }
                        }

                        $hash .= $order_obj->secret_code;

                        echo parent::render(
                            [
                                'order_detail' => $order_obj,
                                'hash' => $hash,
                                'order_item_list' => $order_item_list
                            ]
                        );
                    } else {
                        error(403);
                    }
                } catch (TypeError $e) {
                    error(404);
                }

            } else {
                redirect('/signin/');
            }
        }
    }