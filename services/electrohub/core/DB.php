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
                $this->db_password
            );

            if ($this->connect->connect_error) {
                throw new Exception($this->connect->connect_errno . ': ' . $this->connect->connect_error);
            }

            if (!$this->connect->select_db($this->db_name)) {
                if ($this->connect->query('CREATE DATABASE ' . $this->db_name . '  DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;')) {
                    $this->connect->select_db($this->db_name);

                } else {
                    throw new Exception('Error creating database: ' . $this->connect->error . "\n");
                };
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

    new DB();