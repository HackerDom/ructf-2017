<?php

    function redirect(string $url)
    {
        $url = trim(preg_replace('/\s+/', ' ', $url));
        header('Location: ' . $url);
        exit;
    }

    function error(int $http_code)
    {
        http_response_code($http_code);
        echo '<h1>Error ' . $http_code . '</h1>';
        exit;
    }