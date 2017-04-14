<?php

    function redirect($url)
    {
        $url = str_replace('\n', '', $url);
        $url = str_replace('\r', '', $url);
        header('Location: ' . $url);
        exit;
    }

    function error($http_code)
    {
        http_response_code($http_code);
        echo '<h1>Error ' . $http_code . '</h1>';
        exit;
    }