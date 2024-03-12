//TODO: try to figure out orbitControls + check if the splats turn to the view point


async function fetchAndParsePoints() {
    // Getting points from the splat and storing them into a point array with information about them
    //burek
    const response = await fetch('nike.splat'); //set different parameters for scaling based on the name of the file
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

    //sorting the points based on their distance from the camera
    // points.sort((a, b) => {
    //     const depthA = Math.sqrt(a.position[0]**2 + a.position[1]**2 + a.position[2]**2);
    //     const depthB = Math.sqrt(b.position[0]**2 + b.position[1]**2 + b.position[2]**2);
    //     return depthB - depthA; // Sort in descending order based on depth
    // });

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
        camera.position.set(0,0,5)

        // Order points based on depth (distance from camera)
        const cameraPosition = new THREE.Vector3(); // Assuming you have access to the camera position
        points.sort((a, b) => {
            const depthA = cameraPosition.distanceTo(new THREE.Vector3(...a.position));
            const depthB = cameraPosition.distanceTo(new THREE.Vector3(...b.position));
            return depthB - depthA; // Sort in descending order based on depth
        });

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
            //const scaledPosition = points[i].position.map(coord => coord * scaling_factor);
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
        //pointCloud.scale.set(0.5, 0.5, 0.5);
        pointCloud.position.set(0, 0, 0);

        scene.add(pointCloud);
      
        
        // Render loop
        function animate() {
            requestAnimationFrame(animate);
            //controls.update();
            renderer.render(scene, camera);
        }
        
        animate();
        return scene;
}

function updatePointsGeometry(scene, scaling_factor) {
    // Update point geometry based on the new scaling factor
    const new_size = 0.03 * scaling_factor; // Adjust the base size according to the scaling factor

    // Update size of all existing points
    scene.traverse((object) => {
        if (object instanceof THREE.Points) {
            object.material.size = new_size;
        }
    });
}


async function loadAndInitScene() {
    //scaling factor 
    const def_scaling_factor = 1.0; //default value before user input
    let scaling_factor = def_scaling_factor;
    const scalingSlider = document.getElementById('scaling-slider');

    try {
        const points = await fetchAndParsePoints();
        console.log("Points saved")
        scene = init3DScene(points, scaling_factor);

         // Update scaling factor when the slider value changes
        scalingSlider.addEventListener('input', () => {
        scaling_factor = parseFloat(scalingSlider.value);
        //console.log("Current scaling factor")
        //console.log(scaling_factor);
        updatePointsGeometry(scene, scaling_factor);
        // Call a function to update the points geometry based on the new scaling factor
    });

        
    } catch (error) {
        console.error("Failed to load or initialize the scene:", error);
    }

}

// Function that loads points and initializes the scene.
loadAndInitScene();
