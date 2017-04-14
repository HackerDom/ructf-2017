<?php

    class DB
    {
        public $connect;
        private $db_host;
        private $db_user;
        private $db_password;
        private $db_name;

        function __construct(
            string $db_host = '127.0.0.1',
            string $db_user = 'root',
            string $db_password = '',
            string $db_name = 'ructf'
        )
        {
            $this->db_host = $db_host;
            $this->db_user = $db_user;
            $this->db_password = $db_password;
            $this->db_name = $db_name;

            $this->connect = new mysqli(
                $this->db_host,
                $this->db_user,
                $this->db_password,
                $this->db_name
            );
            if ($this->connect->connect_error) {
                throw new Exception($this->connect->connect_errno . ': ' . $this->connect->connect_error);
            }
        }

        function __destruct()
        {
            $this->connect->close();
        }

        public function query(string $query)
        {
            $result = $this->connect->query($query);
            if ($result === false)
                error('DB query error: ' . $this->connect->error);
            return $result;
        }

        public function escape_value($value)
        {
            return "'" . $this->connect->real_escape_string($value) . "'";
        }
    }
