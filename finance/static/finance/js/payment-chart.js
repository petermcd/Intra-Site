labels = []
values = []

function get_data()
{
    $(".company").each(function(index){
        company_name = $.trim($(this).text());
        if (company_name !== '' && company_name !== 'Company'){
            payment = $(".monthly_payment").get(index).innerText.substring(1);
            if(payment !== '0.00'){
                labels.push(company_name);
                values.push(payment);
            }
        }
    });
}
get_data()
var ctx = document.getElementById('monthly_chart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: 'Monthly Payments',
            data: values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'right'
            }
        }
    }
});