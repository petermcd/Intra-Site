google.charts.load('current', {packages: ['corechart', 'line']});
let data = []

document.body.addEventListener('htmx:beforeSwap', function(evt) {
	if (evt.detail.shouldSwap) {
		const response = JSON.parse(evt.detail.xhr.response);
		for (let i = 0; i < response['record_count']; i++){
			data.push([new Date(response['data'][i]['date']), parseFloat(response['data'][i]['value'])]);
		}
		google.charts.setOnLoadCallback(process_graph);
	}
	evt.detail.shouldSwap = false;
});

function process_graph()
{
	let graph_data = new google.visualization.DataTable();
	graph_data.addColumn('date', 'X');
	graph_data.addColumn('number', document.getElementById('company').innerText);
	graph_data.addRows(data);
	const options = {
		hAxis: {
			title: 'When'
        },
        vAxis: {
          title: 'Balance'
        }
      };

      let chart = new google.visualization.LineChart(document.getElementById('chartContainer'));

      chart.draw(graph_data, options);
}