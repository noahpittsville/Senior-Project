const ctx = document.getElementById("linechart").getContext('2d');
const twit = document.getElementById("linechart2").getContext('2d');


//Grab Cookies
let cookieString = document.cookie;
//Find a Cookie
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// Search result data is in the JS global variable queriedResult. This is an array of objects returned from the DB.
//Parse Data
//Format time
for (x in queriedResult.set1) {
  queriedResult.set1[x].dateTweet = queriedResult.set1[x].dateTweet.split('T')[0]
}
for (x in queriedResult.set2) {
  queriedResult.set2[x].infoDate = queriedResult.set2[x].infoDate.split('T')[0]
}
//Array for combined table
if (queriedResult.set1[0]) {
  var parsedResult = {
    date: [queriedResult.set1[0].dateTweet],
    sentiment: [0.0],
    closePrice:[]
  };

  var node = 0;
  for (var i in queriedResult.set1) {
    if (queriedResult.set1[i].dateTweet != parsedResult.date[node]) {
      //console.log(parsedResult.date[node])
      //console.log(parsedResult.sentiment[node])
      node++
      parsedResult.date[node] = queriedResult.set1[i].dateTweet
      parsedResult.sentiment.push(0.0)
    }

    if (queriedResult.set1[i].sentScore == "Positive") {
      parsedResult.sentiment[node] += 10
    }
    else if (queriedResult.set1[i].sentScore == "Neutral") {
      parsedResult.sentiment[node] += 0
    }
    else if (queriedResult.set1[i].sentScore == "Negative") {
      parsedResult.sentiment[node] += -10
    }

  }
  var checkFound = false;
  //console.log(parsedResult.date.length)
  for (x in parsedResult.date) {
    //console.log(parsedResult.date[x])
    for (y in queriedResult.set2) {
      if (parsedResult.date[x] == queriedResult.set2[y].infoDate) {
        //console.log(queriedResult.set2[y].infoDate)
        parsedResult.closePrice.push(queriedResult.set2[y].closePrice)
        checkFound = true
        break
      }
    }
    if (!checkFound) {
      parsedResult.closePrice.push(parsedResult.closePrice[parsedResult.closePrice.length-1])
    }
    checkFound = false
  }
  const twitChart = new Chart(twit, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
          {
            label: 'Sentiment',
            backgroundColor: 'rgba(161, 198, 247, 0.5)',
            borderColor: 'rgb(47, 128, 237)',
            data: [],
          },
          {
            label: 'Closing Price',
            backgroundColor: 'rgba(255, 25, 25, 0.5)',
            borderColor: 'rgb(255, 25, 25)',
            data: [],

          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
              }
            }]
          }
        },
});

//Add to chart
var testing = "forty"

for(x in parsedResult.date) {
  console.log(parsedResult.sentiment[x])
  twitChart.data.labels.push(parsedResult.date[x])
  twitChart.data.datasets[0].data.push(parsedResult.sentiment[x])
  twitChart.data.datasets[1].data.push(parsedResult.closePrice[x])
}

}

const stockChart = new Chart(ctx, {
  type: 'line',
  data: {
      labels: [],
      datasets: [{
          label: 'Open Price',
          backgroundColor: 'rgba(247, 220, 10, 0.5)',
          borderColor: 'rgb(247, 220, 10)',
          data:[],
        },
        {
          label: 'High Price',
          backgroundColor: 'rgba(253, 155, 0, 0.5)',
          borderColor: 'rgb(253, 155, 0)',
          data:[],
        },
        {
          label: 'Low Price',
          backgroundColor: 'rgba(255, 25, 25, 0.5)',
          borderColor: 'rgb(255, 25, 25)',
          data:[],
        },
        {
          label: 'Close Price',
          backgroundColor: 'rgba(22, 225, 54, 0.75)',
          borderColor: 'rgb(22, 225, 54)',
          data: [],
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
            }
          }]
        }
      },
});

for (x in queriedResult.set2) {
  stockChart.data.labels.push(queriedResult.set2[x].infoDate)
  stockChart.data.datasets[0].data.push(queriedResult.set2[x].openPrice)
  stockChart.data.datasets[1].data.push(queriedResult.set2[x].highPrice)
  stockChart.data.datasets[2].data.push(queriedResult.set2[x].lowPrice)
  stockChart.data.datasets[3].data.push(queriedResult.set2[x].closePrice)
}



