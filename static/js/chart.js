window.onload = function() {
	let dataPoints = [];

	let options =  {
		zoomEnabled: true,
		animationEnabled: true,
		theme: "light2",
		title: {
			text: "Trend"
		},
		axisX: {
			valueFormatString: "DD MMM YYYY",
		},
		axisY: {
			title: "GBP",
			titleFontSize: 24
		},
		data: [{
			type: "spline",
			yValueFormatString: "£#,###.##",
			dataPoints: dataPoints
		}]
	};

	function addData(data) {
		console.log(JSON.stringify(data))
		for (let i = 0; i < data['data'].length; i++) {
			dataPoints.push({
				x: new Date(data['data'][i].data),
				y: Number(data['data'][i].value)
			});
		}
		$("#chartContainer").CanvasJSChart(options);
	}
	$.getJSON("year.json", addData);
}
