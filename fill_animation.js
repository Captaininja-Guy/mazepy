

// Utility Function for waiting
const delay = ms => new Promise(res => setTimeout(res, ms));

async function main(){
    window.pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await pyodide.loadPackage("https://cdn.jsdelivr.net/gh/Captaininja-Guy/mazepy@main/dist/pyodide/the_maze_py-0.2.2-py3-none-any.whl");
    await pyodide.loadPackage('matplotlib');
    await pyodide.runPython(`
        import js
        import mazepy as mp
    `);
    console.log('Done')
}
main()


//The algorithm options that are allowed for each shape of maze
var shapeOptions = {
    "Rectangular": ["Binary Tree", "Sidewinder", "Aldous Broder", "Wilsons", "Recursive Backtrack", "Hunt and Kill",
        "Simplified Prims", "True Prims", "Modified Prims", "Kruskals", "Ellers", "Growing Tree", "Recursive Division", "Origin Shift"],
    
    "Polar": ["Binary Tree", "Sidewinder", "Aldous Broder", "Wilsons", "Recursive Backtrack", "Hunt and Kill",
        "Simplified Prims", "True Prims", "Modified Prims", "Ellers", "Growing Tree", "Origin Shift"],

    "Hexagonal": ["Binary Tree", "Sidewinder", "Aldous Broder", "Wilsons", "Recursive Backtrack", "Hunt and Kill",
        "Simplified Prims", "True Prims", "Modified Prims", "Ellers", "Growing Tree", "Origin Shift"],

    "Triangular": ["Sidewinder", "Aldous Broder", "Wilsons", "Recursive Backtrack", "Hunt and Kill",
        "Simplified Prims", "True Prims", "Modified Prims", "Kruskals", "Growing Tree", "Origin Shift"]
}


//Sends values of selection windows to python whenever they change and sets "Algorithms" with correct algorithms
window.onload = function(){
    const shapeSel = document.getElementById("type");
    const algoSel = document.getElementById("algo");
    const sizeSel = document.getElementById("maze_size");

    for (let x in shapeOptions) {
        shapeSel.options[shapeSel.options.length] = new Option(x, x);
    }
    shapeSel.onchange = function(){
        algoSel.length = 1
        z = shapeOptions[shapeSel.value]
        
        shape_of_cells = shapeSel.value
        for (let i = 0; i < z.length; ++i) {
            algoSel.options[algoSel.options.length] = new Option(z[i], z[i]);
        }
    }
}


function all_options_selected(){
    let shape_option = document.getElementById("type")
    let algorithm_option = document.getElementById("algo")
    let size_option = document.getElementById("maze_size")

    return !(shape_option.options[shape_option.selectedIndex].text == "--Select Maze Shape--" ||
        algorithm_option.options[algorithm_option.selectedIndex].text == "--Select Maze Algorithm--"||
        size_option.options[size_option.selectedIndex].text == "--Select Maze Size--")
}



// Since 'generate' is a submit button, it has a different event listener
document.addEventListener(
        'DOMContentLoaded', () => {
    document.getElementById('gen').
        addEventListener('click', function () {
            if (!all_options_selected())
                alert('Please select all options')
            else
                visible_loader(); //Why is the loader not showing up?!?!?!?
                create_animation();
                invisible_loader();
        });
});

function visible_loader(){
    const loader = document.getElementById("loader");
    const container = document.getElementById("video");
    container.style.visibility = "hidden";
    loader.style.animationPlayState = "running";
    loader.style.visibility = "visible";
}

function invisible_loader(){
    const loader = document.getElementById("loader");
    const container = document.getElementById("video");
    loader.style.animationPlayState = "paused";
    loader.style.visibility = "hidden";
    container.style.visibility = "visible";
}

var size;
var shape;
var algorithm;
var start_color;
var end_color;
function create_animation(){
    let size_selected = document.getElementById("maze_size");
    size_selected = size_selected.options[size_selected.selectedIndex].text;
    switch (size_selected){
    case "Small (6x6)":
        size = 6;
        break;
    case "Medium (12x12)":
        size = 12;
        break;
    case "Large (20x20)":
        size = 20;
    }
    const shape_selected = document.getElementById("type");
    shape = shape_selected.options[shape_selected.selectedIndex].text;
    const algorithm_selected = document.getElementById("algo");
    algorithm = algorithm_selected.options[algorithm_selected.selectedIndex].text;
    
    start_color = document.getElementById("basecolor").value;
    end_color = document.getElementById("endcolor").value;
    let pyodide = window.pyodide

    pyodide.runPython(`
        match js.shape:
            case "Rectangular":
                grid = mp.grids.ColoredGrid(js.size,js.size,base=js.start_color,end=js.end_color)
            case "Polar":
                grid = mp.grids.ColoredPolarGrid(js.size,base=js.start_color,end=js.end_color)
            case "Hexagonal":
                grid = mp.grids.ColoredHexGrid(js.size,js.size, base=js.start_color,end=js.end_color)
            case "Triangular":
                grid = mp.grids.ColoredTriangleGrid(js.size,js.size, base=js.start_color,end=js.end_color)
        algorithm = eval('mp.algorithms.'+js.algorithm.replace(" ", ""))
        algorithm(grid)
        anim = mp.play_fill_2d(grid, show=False)
        string = anim.to_jshtml()
    `);
    
    const string = pyodide.globals.get("string");
    const container = document.getElementById("video");
    container.innerHTML = string
    
    // Execute HTML matplotlib gives
    container.querySelectorAll("script").forEach(oldScript => {
        const newScript = document.createElement("script");

        Array.from(oldScript.attributes).forEach(attr => {
            newScript.setAttribute(attr.name, attr.value);
        });
        
        newScript.appendChild(
            document.createTextNode(oldScript.innerHTML)
        );

        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
}