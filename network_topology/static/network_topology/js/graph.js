const elem = $('#graph')[0];
const topology_graph = ForceGraph3D()
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
     });
topology_graph(elem);

function set_graph_size(){
    topology_graph
        .width(elem.offsetWidth)
        .height(elem.offsetHeight)
}
window.onresize = set_graph_size;