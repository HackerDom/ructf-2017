<?php
    require_once __DIR__ . '/../core/Modal.php';
    require_once __DIR__ . '/../core/ModalField.php';


    class Application extends BaseModel
    {
        public static $table_name = 'application';

        public static function get_schema()
        {
            return array(
                'id' => new IntegerField(
                    ['primary_key' => true, 'auto_increment' => true]
                ),
                'id_machine' => new CharField(array('max_length' => 255)),
                'id_machine' => new CharField(array('max_length' => 255)),
                'user' => new IntegerField()
            );


        }

        public function save()
        {
            $this->user = password_hash($this->password, PASSWORD_BCRYPT);
            return parent::save();
        }

    }