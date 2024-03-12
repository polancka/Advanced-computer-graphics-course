//TODO: try to figure out orbitControls

async function fetchAndParsePoints() {
    // Getting points from the splat and storing them into a point array with information about them
    //burek
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

function calculatePointCloudCenter(points) {
    if (points.length === 0) {
        // Handle the case where there are no points in the cloud
        return new THREE.Vector3();
    }

    // Initialize the sum of positions
    const sum = new THREE.Vector3();

    // Calculate the sum of all point positions
    for (const point of points) {
        const position = new THREE.Vector3().fromArray(point.position);
        sum.add(position);
    }

    // Divide the sum by the number of points to get the average position (center)
    const center = sum.divideScalar(points.length);

    return center;
}


function init3DScene(points) {
    console.log("rendering")

        // Scene setup
        const scene = new THREE.Scene();
        //scene.background = new THREE.Color(0x000000); // e.g., set to black
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Adjust camera position so we can see the points
        camera.position.set(0,0,10)

        // //const controls = new OrbitControls(camera, renderer.domElement);
        // controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
        // controls.dampingFactor = 0.25; // increase for more damping, decrease for less
        // controls.screenSpacePanning = false; // enable or disable the screen-space panning
        // controls.maxPolarAngle = Math.PI / 2; 

        //Points representation:
        
        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];

       for(let i = 0; i < points.length; i++) {
            // Add positions
            positions.push(...points[i].position);
            const color = new THREE.Color();
            color.setRGB(points[i].color[0] / 255, points[i].color[1] / 255, points[i].color[2] / 255);
            colors.push(color.r, color.g, color.b);
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        
        const material = new THREE.PointsMaterial({ size: 0.03, vertexColors: true });
        const pointCloud = new THREE.Points(geometry,material);

        //translate/rotate/scale
        pointCloud.rotateX(2*Math.PI/3);
        pointCloud.scale.set(2, 2, 2);
        pointCloud.position.set(0, 0, 0);

        scene.add(pointCloud);
      
        
        // Render loop
        function animate() {
            requestAnimationFrame(animate);
            //controls.update();
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
