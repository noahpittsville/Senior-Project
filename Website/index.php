<!DOCTYPE html>
<html lang="en">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/stylelogin.css">
    <?php
        require_once("config.php");
        $testVal = "";
        $reportVar = "";        

        #Initial testing code for CURL communication
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_URL, "localhost:3680/test");

        set_include_path(get_include_path() . ":/home/fac/nick/public_html/3680/include/");
        include_once("FormBuilder.php");
        
        $loginForm = new PhpFormBuilder();
        $loginForm->set_att('id', 'login');
        $loginForm->add_input('Name:', array(), 'userName');
        $loginForm->add_input('Password:', array(), 'passWord');
        $loginForm->add_input('login', array(
            "type"=>"submit",
            "value"=>"Login"
        ), 'Login');

        $regButton = new PhpFormBuilder();
        $regButton->set_att('id', 'regButton');
        $regButton->add_input('register', array(
            "type"=>"submit",
            "value"=>"Register New Account"
        ), 'RegisterNew');

        $regForm = new PhpFormBuilder();
        $regForm->set_att('id', 'regNew');
        $regForm->add_input('Name:', array(),'firstName');
        $regForm->add_input('     ', array(), 'lastName');
        $regForm->add_input('UserName:', array(), 'userName');
        $regForm->add_input('Password:', array(), 'passWord1');
        $regForm->add_input('Confirm Password:', array(), 'passWord2');
        $regForm->add_input('Register', array(
            "type"=>"submit",
            "value"=>"Register Account"
        ), 'regSubmit');

        #Code for posting account creation credentials to the express app.
        if (isset ($_REQUEST["regSubmit"])) {
                $cs = curl_init();
                curl_setopt($cs, CURLOPT_RETURNTRANSFER, 1);
                curl_setopt($cs, CURLOPT_POST, 1);
                $dataString = [
                    "firstName" => $_POST["firstName"],
                    "lastName" => $_POST["lastName"],
                    "userName" => $_POST["userName"],
                    "passWord" => password_hash($_POST["passWord1"], PASSWORD_DEFAULT)
                ];
                $postData = http_build_query($dataString);
                curl_setopt($cs, CURLOPT_POSTFIELDS, $postData);
                curl_setopt($cs, CURLOPT_URL, "localhost:3680/create");
                if ($_POST["passWord1"] == $_POST["passWord2"]) {
                    $testVal = curl_exec($cs);
                }
                else {
                    $reportVar = "Passwords do not match";
                }

        }
        #Code for requesting and verifying passwords stored in DB
        if (isset ($_REQUEST["Login"])) {
            $clog = curl_init();
            curl_setopt($clog, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($clog, CURLOPT_POST, 1);
            $dataString = [
                "userName" => $_POST["userName"]
            ];
            $postData = http_build_query($dataString);
            curl_setopt($clog, CURLOPT_POSTFIELDS, $postData);
            curl_setopt($clog, CURLOPT_URL, "localhost:3680/verify");

            $password = curl_exec($clog);

            if (password_verify($_POST["passWord"], $password)) {
                $Success = "It worked<br>";
                curl_reset($clog);
                curl_setopt($clog, CURLOPT_RETURNTRANSFER, 1);
                curl_setopt($clog, CURLOPT_POST, 1);
                curl_setopt($clog, CURLOPT_POSTFIELDS, $postData);
                curl_setopt($clog, CURLOPT_URL, "localhost:3680/grabInfo");
                $userInfo = json_decode(curl_exec($clog));
                $_SESSION["loggedIn"] = true;
                $_SESSION["firstName"] = $userInfo->firstName;
                $_SESSION["lastName"] = $userInfo->lastName;
                $_SESSION["userName"] = $userInfo->userName;
                header("location: userHome.php");
                
            }
            #else $Success = "Wrong Password<br>";
        }

    ?>
    <head>
            <title>Senior Project: Twitter Sentiment and Stock</title>
    </head>
    <body>
            <div class ="container-fluid">
                <div class="row">
                    <div class="col-sm-12">
                        <!--<h1>SP: Twitter Sentiment and Stock</h1>-->
                    </div>
                </div>
            </div>
            <div class ="container">
                <div class="row">
                    <h1>SP: Twitter Sentiment and Stock</h1>
                    <div class="col-sm-1">
                        <!--Spacer-->
                        <?php 
                            #echo curl_exec($ch);
                            #echo $testVal;
                            #echo $reportVar;
                            #echo $testVariable;
                            #echo $Success;
                            #echo $userInfo->lastName;
                            #print_r($_SESSION);
                        ?>
                    </div>
                    <div class="col-sm-3">
                        <?php $loginForm->build_form();
                              $regButton->build_form();
                              $regForm->build_form();
                        ?>
                        <style> #regNew{display: None;}</style>
                        <?php 
                            if (isset($_REQUEST["RegisterNew"])) {
                                echo '<style> #login{display: None;} </style>';
                                echo '<style> #regButton{display: None;} </style>';
                                echo '<style> #regNew{display: Block;} </style>';
                            }
                        ?>
                    </div>
                </div>
            </div>
    </body>
</html>
