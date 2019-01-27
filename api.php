<?php
header("Content-Type:application/json");
require "backend.php";


if (isset($_POST['confirm'])){

    $id = $_POST['confirm'];
    if (mysqli_num_rows($queue) > 0) {
        // output data of each row

        $queues = '[';

        while($row = mysqli_fetch_assoc($queue)) {
            $queues = $queues . $row['json'] . ',';
        }
        $queues = $queues . '{"id": 0}';
        $queues = $queues . ']';
        $queues = '{'.'"queues":'.$queues.'}';
        echo $queues;

        dequeue($id);
    }
}

if (isset($_POST['api'])){
    $api_request = $_POST['api'];

    if ($api_request == 'history'){

        $q = 'SELECT json FROM history';
        $q = mysqli_query($conn, $q);
        
        if (mysqli_num_rows($q) > 0){

            $queues = '[';

            while($row = mysqli_fetch_assoc($q)){
                $queues = $queues . $row['json'] . ',';
            }

            $queues = $queues . '{"id": 0}';
            $queues = $queues . ']';
            $queues = '{'.'"queues":'.$queues.'}';
            echo $queues;
            
        } else {
            echo 'API ERROR';
        }
    }

    if (isset($_POST['query'])){
        if ($api_request == 'query'){
            $query = $_POST['query'];
            $q = mysqli_query($conn, $query);

            if (mysqli_num_rows($q) > 0){

                $queues = '[';
    
                while($row = mysqli_fetch_assoc($q)){
                    $queues = $queues . $row['json'] . ',';
                }
    
                $queues = $queues . '{"id": 0}';
                $queues = $queues . ']';
                $queues = '{'.'"queues":'.$queues.'}';
                echo $queues;
                
            } else {
                echo 'API ERROR';
            }
        }
    }
}



?>