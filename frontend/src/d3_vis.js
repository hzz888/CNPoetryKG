// Popoto.js configuration.
var driver = neo4j.driver(
    "bolt://localhost:7687",
    neo4j.auth.basic("neo4j", "123456"),
);

popoto.runner.DRIVER = driver

popoto.provider.node.Provider = {
    "作者": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name",
        "autoExpandRelations": true // if set to true Person nodes will be automatically expanded in graph
    },
    "标题": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name",
        "autoExpandRelations": true
    },
    "作者简介": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "分类": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "创作背景": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "朝代": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
        
    },
    "诗词内容": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name",
        "autoExpandRelations": true
    },
    "译文": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "赏析": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "喜悦因子": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "愤怒因子": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "厌恶因子": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    },
    "悲伤因子": {
        "returnAttributes": ["name"],
        "constraintAttribute": "name"
    }
};

driver.verifyConnectivity().then(function () {
    // Start the generation using parameter as root label of the query.
    popoto.start("标题");
}).catch(function (error) {
    document.getElementById("modal").style.display = "block";
    document.getElementById("error-content").innerText = error;
    console.error(error)
})

popoto.result.onTotalResultCount(function (count) {
    document.getElementById("result-total-count").innerHTML = "(" + count + ")";
});
popoto.query.RESULTS_PAGE_SIZE = 100;

// Below is neovis.js configuration.
var viz;

function draw() {
    var config = {
        container_id: "viz",
        server_url: "bolt://localhost:7687",
        server_user: "neo4j",
        server_password: "123456",
        labels: {
            //"Character": "name",
            "标题": {
                "caption": "name",
                "size": 30,
                "title_properties": [
                    "name",
                    // "pagerank"
                ]
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "作者": {
                "caption": "name",
                "size": 40,
                // "community": "community",
                // "sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "作者简介": {
                "caption": "name",
                "size": 40,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "分类": {
                "caption": "name",
                "size": 30,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "创作背景": {
                "caption": "name",
                "size": 30,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "朝代": {
                "caption": "name",
                "size": 40,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "译文": {
                "caption": "name",
                "size": 30,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "诗词内容": {
                "caption": "name",
                "size": 30,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "赏析": {
                "caption": "name",
                "size": 30,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "喜悦因子": {
                "caption": "name",
                "size": 20,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "愤怒因子": {
                "caption": "name",
                "size": 20,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "厌恶因子": {
                "caption": "name",
                "size": 20,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
            "悲伤因子": {
                "caption": "name",
                "size": 20,
                // "community": "community"
                //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
            },
        },
        relationships: {
            "诗词作者": {
                "thickness": "weight",
                "caption": true
            },
            "作者朝代": {
                "thickness": "weight",
                "caption": true
            },
            "作者简介": {
                "thickness": "weight",
                "caption": true
            },
            "创作背景": {
                "thickness": "weight",
                "caption": true
            },
            "朝代": {
                "thickness": "weight",
                "caption": true
            },
            "译文": {
                "thickness": "weight",
                "caption": true
            },
            "诗词内容": {
                "thickness": "weight",
                "caption": true
            },
            "诗词分类": {
                "thickness": "weight",
                "caption": true
            },
            "赏析": {
                "thickness": "weight",
                "caption": true
            },
            "喜悦因子为": {
                "thickness": "weight",
                "caption": true
            },
            "愤怒因子为": {
                "thickness": "weight",
                "caption": true
            },
            "厌恶因子为": {
                "thickness": "weight",
                "caption": true
            },
            "悲伤因子为": {
                "thickness": "weight",
                "caption": true
            },
        },

        initial_cypher: "match(n {name:'李白'})-[r]-(p) return n,r,p limit 50"
    };

    viz = new NeoVis.default(config);
    viz.render();
    console.log(viz);

}

$("#reload").click(function () {

    var cypher = $("#cypher").val();

    if (cypher.length > 3) {
        viz.renderWithCypher(cypher);
    } else {
        console.log("reload");
        viz.reload();

    }

});

$("#stabilize").click(function () {
    viz.stabilize();
})