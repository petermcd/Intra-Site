const elem = $('#graph')[0];
const topology_graph = ForceGraph3D()
    (elem)
    .jsonUrl('/network/topology.json')
    .nodeAutoColorBy('type')
    .width(elem.offsetWidth)
    .height(elem.offsetHeight)
    .linkWidth(link => `2`)
    .nodeThreeObject(node => {
        const sprite = new SpriteText(node.name);
        sprite.material.depthWrite = false;
        sprite.color = node.color;
        sprite.textHeight = 6;
        return sprite;
     })
    .onNodeClick(node => {
        // Aim at node from outside it
        const distance = 200;
        const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
        topology_graph.cameraPosition(
            { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
            node,
            3000
        );
        output_details(node)
    });

function set_graph_size(){
    topology_graph
        .width(elem.offsetWidth)
        .height(elem.offsetHeight)
}
function output_details(node){
    let elem = $('#graph-item-details');
    let details = '<h2>Details</h2>';
    if(node.type === 'site'){
        details = details +
            'Name: <a href="' + node.url + '">' + node.name + '</a><br />' +
            'Description: ' + node.description + '<br />';
    }
    else if(node.type === 'device'){
        details = details +
            'Name: ' + node.name + '<br />' +
            'IP: ' + node.ip + '<br />' +
            'Description: ' + node.description + '<br />';
    }
    elem.html(details);
}
window.onresize = set_graph_size;