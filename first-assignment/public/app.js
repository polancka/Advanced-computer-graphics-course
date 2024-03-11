async function fetchAndParsePoints() {
    // Getting points from the splat and storing them into a point array with information about them
    const response = await fetch('nike.splat');
    const arrayBuffer = await response.arrayBuffer();
    const data = new DataView(arrayBuffer);

    const points = [];
    const pointSize = 32; // Each point is 32 bytes

    for (let offset = 0; offset < data.byteLength; offset += pointSize) {
        const position = [
            data.getFloat32(offset, true),
            data.getFloat32(offset + 4, true),
            data.getFloat32(offset + 8, true),
        ];
        const scale = [
            data.getFloat32(offset + 12, true),
            data.getFloat32(offset + 16, true),
            data.getFloat32(offset + 20, true),
        ];
        const color = [
            data.getUint8(offset + 24),
            data.getUint8(offset + 25),
            data.getUint8(offset + 26),
            data.getUint8(offset + 27),
        ];
        const rotation = [
            (data.getUint8(offset + 28) - 128) / 128.0,
            (data.getUint8(offset + 29) - 128) / 128.0,
            (data.getUint8(offset + 30) - 128) / 128.0,
            (data.getUint8(offset + 31) - 128) / 128.0,
        ];

        points.push({ position, scale, color, rotation });
    }
    console.log("Got points")
    return points;
}

function init3DScene(points) {
    console.log("rendering")

        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x000000); // e.g., set to black
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Adjust camera position so we can see the points
        camera.position.z = 10;
        
        // Create a geometry for each point
        for(let i = 0; i < 15000; i++ ){
            const geometry = new THREE.SphereGeometry(0.01, 32, 32); // Small sphere geometry to represent the point
            const [r, g, b, a] = points[i].color;
            const colorHex = (r << 16) | (g << 8) | b;
    
            const material = new THREE.MeshBasicMaterial({
            color: colorHex,
            opacity: a / 255, // Convert alpha from [0, 255] to [0, 1]
            transparent: true, // Need to set transparent to true to use opacity
            });
            //const material = new THREE.MeshBasicMaterial({ color: 0xff0000 }); // Red color for visibility
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.set(...points[i].position);
            scene.add(sphere);
            //console.log(points[i].position)

        }
    
        
        // Render loop
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        
        animate();
}


async function loadAndInitScene() {
    try {
        const points = await fetchAndParsePoints();
        console.log("Points saved")
        init3DScene(points);
    } catch (error) {
        console.error("Failed to load or initialize the scene:", error);
    }
}

// Function that loads points and initializes the scene.
loadAndInitScene();
