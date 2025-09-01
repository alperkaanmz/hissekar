// Django görünümünden JSON verisini al
    var jsonData = JSON.parse('{{ json_data | escapejs }}');

    // Grafik verilerini ayarla
    var options = {
        series: [{
            name: "Stock Price",
            data: jsonData.prices.map(item => item.close)
        }],
        chart: {
            height: 400,
            type: 'line',
        },
        xaxis: {
            categories: jsonData.prices.map(item => item.date)
        }
    };

    // Grafik oluştur
    var chart = new ApexCharts(document.querySelector("#chart-container"), options);
    chart.render();

    // Sayfada görüntülenecek olan diğer bilgileri güncelle
    document.getElementById("current-price").innerText = "Current Price: $" + jsonData.current_price;
    document.getElementById("symbol").innerText = jsonData.symbol + " Profile";
