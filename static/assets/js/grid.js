(function () {
    'use script';

  

    // with sorting
    new gridjs.Grid({
        pagination: true,
        search: true,
        sort: true,
        columns: [{
            name: "Şirket",
            width: "150px",
        }, {
            name: "Rasyo1",
            width: "150px",
        }, {
            name: "Rasyo2",
            width: "200px",
        }, {
            name: "Rasyo3",
            width: "150px",
        }, {
            name: "Rasyo4",
            width: "100px",
        }, {
            name: "Rasyo5",
            width: "100px",
        }, 
        {
            name: "Rasyo5",
            width: "100px",
        },
        {
            name: "Rasyo5",
            width: "100px",
        },{
            name: "Rasyo6",
            width: "100px",
        }],
        data: [
            ["ALARK", "john", "john123@gmail.com", "#12012", "$1799", "1", "$1799"],
            ["ARCLK", "mark", "markzenner23@gmail.com", "#12013", "$2479", "2", "$4958"],
            ["ASELS", "eoin", "eoin1992@gmail.com", "#12014", "$769", "1", "$769"],
            ["ASTOR", "sarahcdd", "sarahcdd129@gmail.com", "#12015", "$1299", "3", "$3997"],
            
        ],
    }).render(document.getElementById("grid-sorting"));;
    // with sorting

   
})();