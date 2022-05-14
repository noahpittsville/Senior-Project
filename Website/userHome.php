<!doctype html>
<html lang="en">
    <?php 
        require_once("config.php");

        $chartSearch = "";
        $sideBarList ="";

        if (isset ($_GET["companyID"])) {
            $cs = curl_init();
            curl_setopt($cs, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($cs, CURLOPT_POST, 1);
            $dataString = [
                "companyID" => $_GET["companyID"],
                "startDate" => $_GET["startDate"],
                "endDate" => $_GET["endDate"]
            ];
            $postData = http_build_query($dataString);
            curl_setopt($cs, CURLOPT_POSTFIELDS, $postData);
            curl_setopt($cs, CURLOPT_URL, "localhost:3680/grabChartInfo");
            $chartSearch = curl_exec($cs);
            //setcookie("queriedCookie", $_GET["companyID"]);

            $searchArray = json_decode($chartSearch, true);
            $chartSearch = json_encode($searchArray);

            
            echo "<script>
            var queriedResult = $chartSearch;
            </script>";
        }

        if(!isset($_SESSION['userName'])) {
            header("location: index.php");
        }

        if (isset ($_SESSION['userName'])) {
            $cSavStk = curl_init();
            curl_setopt($cSavStk, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($cSavStk, CURLOPT_POST,1);
            $dataString = ["userName" => $_SESSION["userName"]];
            $postData = http_build_query($dataString);
            curl_setopt($cSavStk, CURLOPT_POSTFIELDS, $postData);
            curl_setopt($cSavStk, CURLOPT_URL, "localhost:3680/grabTrackInfo");
            $savedStock = curl_exec($cSavStk);
            $savedStockDecoded = json_decode($savedStock, true);
            foreach ($savedStockDecoded as $loop) {
                $temp = $loop["stockID"];
                $sideBarList .= "
                    <li>
                        <a href=\"https://cs.csubak.edu/~njackson/3680/project3/userHome.php?companyID=$temp\" class=\"nav-link\">
                            <span class=\"me-2\">
                                <i class=\"bi bi-layout-split\"></i>
                            </span>
                            <span>$temp</span>
                        </a>
                    </li>
                ";
            }

        }
    ?>

  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.11.5/datatables.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">

        <!-- JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.js"></script>
    <script src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"></script>

    <script src="https://cdn.datatables.net/1.11.3/js/dataTables.bootstrap5.min.js"></script>


    <link rel="stylesheet" href="css/style.css" />
    <script>
    console.log(queriedResult);

        function searchStock(evt) {
            //evt.preventDefault();

            let searchingFor = document.getElementById("submit-stock-name").value;
            let startDate = document.getElementById("startDate").value;
            let endDate = document.getElementById("endDate").value;
             

            let newListItem = `
                <li>
                    <a href="#" class="nav-link">
                        <span class="me-2">
                            <i class="bi bi-layout-split"></i>
                        </span>
                        <span>${searchingFor}</span>
                    </a>
                </li>
                `;
            let savedStocks = document.getElementById("savedStockList");
            savedStocks.innerHTML += newListItem;

            postSearchInfo();
        }

        async function postSearchInfo(evt) {
            //evt.preventDefault();
            let searchingFor = document.getElementById("submit-stock-name").value;
            let startDate = document.getElementById("startDate").value;
            let endDate = document.getElementById("endDate").value;

            window.location=`https://cs.csubak.edu/~njackson/3680/project3/userHome.php?companyID=${searchingFor}&startDate=${startDate}&endDate=${endDate}`;
            //let returnData = await fetch(`https://cs.csubak.edu/~njackson/3680/project3/userHome.php/?companyID=${searchingFor}&startDate=${startDate}&endDate=${endDate}`);
            /*
            .then(response => {
                response.text();
                console.log(data)
            })
            .catch(error => {
                console.log(error);
            });
           console.log(returnData.text());
           console.log('Runs');
           */
        }
    </script>
    <script type="text/javascript">
        /*
        $(function() {
            $("#datepicker").datepicker();
        });
        */
    </script>

    <title>Sentiment & Stock SP</title>
  </head>
  <body>
    <!-- navbar -->
        <!-- // fixed-top will make the navbar alway show even when scrolling the main -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <!-- offcanvas trigger ~ here so button goes away if offcanvas is triggered  // me-2 add space between button and Project Name -->
            <button class="navbar-toggler me-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
                <span class="navbar-toggler-icon" data-bs-target="#offcanvasExample"></span>
            </button>
            <!-- end offcanvas trigger -->
                <!-- // me-auto pushes Project Name to the left -->
            <a class="navbar-brand fw-bold text-uppercase me-auto" >Sentiment & Stock SP</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <!-- DATEPCIKER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
                <label for="startDate" class="col-sm-1 col-form-label">Date</label>
                <form class="d-flex ms-auto" method="POST">
                    <!-- Search bar with button on the right
                        // my-3 adds room between input box and top button
                        // my-lg-0 makes the sidebar permanent if screen is large enough to fit it,
                            top-left dropdown button disappears -->
                    <div class="input-group date" id="datepicker">
                        <label>From:</label><input type="date" class="form-control" id="startDate" name="startDate">
                        <span class="input-group-append">
                            <!--<span class="input-group-text bg-white d-block">
                                <i class="bi bi-calendar-plus-fill"></i>
                            </span>-->
                        </span>
                    </div>
                    <div class="input-group date" id="datepicker">
                        <label>To:</label><input type="date" class="form-control" id="endDate" name="endDate">
                        <span class="input-group-append">
                            <!--<span class="input-group-text bg-white d-block">
                                <i class="bi bi-calendar-plus-fill"></i>
                            </span>-->
                        </span>
                    </div>
                    &nbsp;
                    <div class="input-group my-3 my-lg-0">
                        <input type="text" class="form-control" id="submit-stock-name" placeholder="Stock Name" aria-label="Stock Name" aria-describedby="button-addon2">
                        <button class="btn btn-outline-primary" id="btn-submit" type="button" onclick = searchStock()>
                            <!-- image of magnifying glass -->
                            <i class="bi bi-search"></i>
                        </button>
                        <script>
                            let btn = document.getElementById("btn-submit");
                            /*
                            <!-- QUERY NAME -->
                            btn.addEventListener('click', event => {
                            searchStock(event);
                            <!-- END QUERY NAME -->
                            <!-- DATE -->
                            <!--btn.addEventListener('click', event => {
                            searchStock(event);-->
                            <!-- END DATE -->
                            })
                            */
                        </script>
                    </div>
                    <!-- <input type="submit" name="submitStartDate" value="Search"> -->
                    <!-- </div> -->
                </form>
                <!-- end DATEPICKER -->
                <!-- // ms-auto moves it to the right -->
                <form class="d-flex ms-auto">
                    <!-- Search bar with button on the right 
                        // my-3 adds room between input box and top button 
                        // my-lg-0 makes the sidebar permanent if screen is large enough to fit it, 
                            top-left dropdown button disappears -->
                    
                </form>
                <ul class="navbar-nav mb-2 mb-lg-0">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <!-- image of person for user -->
                            <i class="bi bi-person-fill"></i>
                        </a>
                        <!-- dropdown-menu-end pushes it on the right of the screen -->
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <!-- divider -->
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="#">Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- end navbar -->

    <!-- offcanvas -->
    <div class="offcanvas offcanvas-start bg-dark text-white sidebar-nav" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
        
        <div class="offcanvas-body p-0">
            <nav class="navbar-dark">
                <ul class="navbar-nav">
                    <li>
                        <div class="text-muted small fw-bold text-uppercase px-3">
                            Core
                        </div>
                    </li>
                    <li>
                        <!-- "#" current link -->
                        <a href="#" class="nav-link px-3 active">
                            <span class="me-2">
                                <i class="bi bi-bank2"></i>
                            </span>
                            <span>Dashboard</span>
                        </a>
                    </li>
                    <!-- divider -->
                    <li class="my-4">
                        <hr class="dropdown-divider" />
                    </li>
                    <li>
                        <div class="text-muted small fw-bold text-uppercase px-3">
                            Repository
                        </div>
                    </li>
                    <li>
                        <a class="nav-link px-3 sidebar-link" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">
                            <!-- -->
                            <span class="me-2">
                                <i class="bi bi-book-fill"></i>
                            </span>
                            <span>Saved Stocks</span>
                            <!-- downwards carot to indicate it is a dropdown link -->
                            <span class="dropdown-icon ms-auto">
                                <i class="bi bi-caret-down-fill"></i>
                            </span>

                        </a>
                        <div class="collapse" id="collapseExample">
                            <div>
                                <ul class="navbar-nav ps-3" id="savedStockList">
                                    <?php echo $sideBarList;
                                    //echo var_dump($savedStockDecoded)?>
                                    <!--<li>
                                        <a href="#" class="nav-link">
                                            <span class="me-2">
                                                <i class="bi bi-layout-split"></i>
                                            </span>
                                            <span>STOCK 1</span>
                                        </a>
                                    </li>
                                    <li>
                                    <a href="#" class="nav-link">
                                            <span class="me-2">
                                                <i class="bi bi-layout-split"></i>
                                            </span>
                                            <span>STOCK </span>
                                        </a>
                                    </li>-->
                                </ul>
                            </div>
                        </div>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
    <!-- end offcanvas -->
    <main class="mt-5 pt-3">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12 fs-3 fw-bold">Dashboard</div>
            </div>
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            Stock Chart
                        </div>
                        <!--<div class="card-body">
                            <canvas class="linechart" width="400" height="200"></canvas>
                        </div>-->
                        <div class="card chart-container">
                            <canvas id="linechart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            Twitter Chart
                        </div>
                        <div class="card chart-container">
                            <canvas id="linechart2"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            Test Chart
                        </div>
                        <div class="card chart-container">
                            <?php 
                            
                            if (strlen($chartSearch) > 0) {
                                echo $chartSearch . "<br>";
                            }
                            
                            ?>
                            <canvas id="linechart3"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>


    <script src="js/lineChart.js"></script>

    
  
  
  </body>
</html>
