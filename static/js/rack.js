// jshint esversion: 6
$.getJSON( "/network/rack.json", function( data ) {
  process_data(data);
});
function process_data(shelf_data) {
    let container = $('#rack');
    let row_iter = 0;
    while (row_iter < 19) {
        row_iter++;
        let row_id = ' id="shelf' + row_iter + '"';
        const row = '<div class="row rack_row"' + row_id + '></div>';
        container.append(row);
    }
    let tab_index = 1;
    for (let shelf in shelf_data) {
        const col_width = 100 / shelf_data[shelf]['width'];
        const row = $('#shelf' + shelf);
        let col_iter = 0;
        while (col_iter < shelf_data[shelf]['width']) {
            col_iter++;
            let col = '<div class="rack_column" style="width: ' + col_width + '%"></div>';
            if (col_iter in shelf_data[shelf]['devices']) {
                const device = shelf_data[shelf]['devices'][col_iter];
                col = '<div class="rack_column" style="width: ' + col_width + '%">' +
                    '<a href="#" data-toggle="' + device['hostname'] + '" data-trigger="focus" title="' + device['hostname'] + '" data-content="ip = ' + device['ip'] + '\n' + device['description'] + '">' +
                    '<img class="device_image" src="' + device['image'] + '" alt="' + device['hostname'] + '">' +
                    '</a></div>';
                row.append(col);
                $('[data-toggle="' + device['hostname'] + '"]').popover();
            }
            else {
                row.append(col);
            }
            tab_index++;
        }
    }
}
