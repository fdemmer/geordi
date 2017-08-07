window.onload = function() {
  var options = {
    "interaction": {
      "hover": true,
      "multiselect": true
    },
    "layout": {
      "improvedLayout": true,
      "randomSeed": 1
    },
    "autoResize": true,
    "edges": {
      "hoverWidth": 2,
      "physics": true,
      "font": {
        "align": "horizontal",
        "size": 25,
        "face": "Arial"
      },
      "smooth": {
        "roundness": 0.25,
        "forceDirection": "vertical",
        "type": "diagonalCross"
      },
      "labelHighlightBold": true
    },
    "manipulation": false,
    "nodes": {
      "scaling": {
        "max": 30,
        "label": {
          "max": 75,
          "maxVisible": 30,
          "enabled": true,
          "drawThreshold": 5,
          "min": 25
        },
        "min": 10
      },
      "shape": "box",
      "font": {
        "color": "white",
        "align": "center",
        "size": 25,
        "face": "Arial"
      },
      "physics": true,
      "size": 150
    },
    "physics": {
      "hierarchicalRepulsion": {
      "nodeDistance": 500,
      "springLength": 190,
        "centralGravity": 0
      },
      "minVelocity": 15,
      "solver": "hierarchicalRepulsion"
    }
  };

  var parsed = vis.network.convertDot(document.getElementById("graph").dataset.dotstring);

  for (var i = 0; i < 2; i++) {
    var elements = parsed[['nodes', 'edges'][i]];
    for (var j = 0; j < elements.length; j++) {
      // https://github.com/almende/vis/issues/3015
      elements[j].label = elements[j].label.replace(/\\n/g, '\n');
    }
  }

  var data = {
    nodes: new vis.DataSet(parsed.nodes),
    edges: new vis.DataSet(parsed.edges)
  };

  var network = new vis.Network(document.getElementById('graph'), data, options);
  network.on('stabilized', function () {
    document.getElementById('spinner').hidden = true;
    document.getElementById('freeze').hidden = true;
  });
  network.on('startStabilizing', function () {
    document.getElementById('freeze').hidden = false;
  });
  document.getElementById('freeze').onclick = function () {
    network.stopSimulation();
  };
  document.onkeydown = function (e) {
    e = e || window.event;
    if (e.key.toLowerCase() === "s") {
      network.stopSimulation();
    }
  };
};
