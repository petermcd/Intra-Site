window.onload = function() {

	var dataPoints = [];

	var options =  {
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
		for (var i = 0; i < data['data'].length; i++) {
			dataPoints.push({
				x: new Date(data['data'][i].date),
				y: Number(data['data'][i].value)
			});
		}
		$("#chartContainer").CanvasJSChart(options);
	}
	$.getJSON("year.json", addData);
}
