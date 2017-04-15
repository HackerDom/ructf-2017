<?php

    class Route
    {
        public $method;
        public $path;
        public $callback;

        public function __construct($method, $path, $callback)
        {
            $this->method = $method;
            $this->path = $path;
            $this->callback = $callback;

        }
    }

    class Router
    {
        public $routes = array();

        public function add_route(string $url, $controller)
        {
            $this->routes[$url] = $controller;
        }

        private function check_part_route(array $route_parts, array $url_parts)
        {
            if (count($route_parts) != count($url_parts)) {
                return false;
            }
            $option = [];
            for ($i = 0; $i < count($route_parts); $i++) {
                $route_part = $route_parts[$i];
                $url_part = $url_parts[$i];

                if (substr($route_part, 0, 1) === ':') {
                    $option [substr($route_part, 1)] = $url_part;
                    break;
                }

                if ($route_part != $url_part) {
                    return false;
                }

            }
            return $option;
        }

        public function find(string $url)
        {
            $pos = strpos($url, '?');
            if ($pos !== false)
                $url = substr($url, 0, $pos);
            foreach ($this->routes as $route_name => $controller) {
                $route_parts = explode('/', $route_name);
                $url_parts = explode('/', $url);
                $result = $this->check_part_route($route_parts, $url_parts);
                if ($result !== false) {
                    return new $controller($result);
                }
            }
        }
    }