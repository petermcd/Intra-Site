// jshint esversion: 6

let shelf_data = {
    1: {
        width: 1,
        devices: {
            1: {
                hostname: 'switch',
                image: 'switch.png'
            }
        }
    },
    2: {
        width: 3,
        devices: {
            1: {
                hostname: 'test',
                image: 'raspberry_pi.png'
            },
            3: {
                hostname: 'test2',
                image: 'raspberry_pi.png'
            }
        }
    }
}
let container = $('#rack');
let row_iter = 0;
while (row_iter < 19){
    row_iter++;
    let row_id = ' id="shelf' + row_iter + '"'
    const row = '<div class="row rack_row"' + row_id + '></div>';
    container.append(row);
}
let tab_index = 1;
for (let shelf in shelf_data){
    const col_width = 100 / shelf_data[shelf]['width']
    const row = $('#shelf' + shelf);
    let col_iter = 0;
    while (col_iter < shelf_data[shelf]['width']) {
        col_iter++;
        let col = '<div class="rack_column" style="width: ' + col_width + '%"></div>';
        if (col_iter in shelf_data[shelf]['devices']){
            const device = shelf_data[shelf]['devices'][col_iter];
            col = '<div class="rack_column" style="width: ' + col_width + '%">' +
                '<img class="device_image" src="/static/networkv2/img/' + device['image'] + '" alt="' + device['hostname'] + '">' +
                '</div>';
        }
        row.append(col);
        tab_index++;
    }
}
