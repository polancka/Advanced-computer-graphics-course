//TODO: try to figure out orbitControls 
async function fetchAndParsePoints() {
    // Getting points from the splat and storing them into a point array with information about them
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


    console.log("Got points")
    return points;
}

//function for calculating the distance between a point and a camera 
function calculateDistance(point, cameraX, cameraY, cameraZ) {
    // Calculate Euclidean distance between a point and the camera
    const dx = point.position[0] - cameraX;
    const dy = point.position[1] - cameraY;
    const dz = point.position[2] - cameraZ;
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

// function calculatePointCloudCenter(points) {
//     if (points.length === 0) {
//         // Handle the case where there are no points in the cloud
//         return new THREE.Vector3();
//     }

//     // Initialize the sum of positions
//     const sum = new THREE.Vector3();

//     // Calculate the sum of all point positions
//     for (const point of points) {
//         const position = new THREE.Vector3().fromArray(point.position);
//         sum.add(position);
//     }

//     // Divide the sum by the number of points to get the average position (center)
//     const center = sum.divideScalar(points.length);

//     return center;
// }


function init3DScene(points) {

    console.log("rendering")
        const camera_x = 0;
        const camera_y = 0;
        const camera_z = 5;         

        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff); // e.g., set to black
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Adjust camera position
        camera.position.set(camera_x,camera_y,camera_z)

        // TODO: Order points based on depth (distance from camera)  --> min to max and vice versa pictures!
        points.sort((a, b) => { //pairwise sort
            const distanceA = calculateDistance(a, camera_x, camera_y, camera_z);
            const distanceB = calculateDistance(b, camera_x, camera_y, camera_z);
            return distanceB - distanceA;
        });

        console.log(points[1].position);
        console.log(points[2].position);

        //TODO: Manual controls using orbit controls - dependencies issues
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
            // // Add positions
            // //const scaledPosition = points[i].position.map(coord => coord * scaling_factor);
            // positions.push(...points[i].position);

            // //TODO: implement alpha blending
            // const color = new THREE.Color();
            // color.setRGB(points[i].color[0] / 255, points[i].color[1] / 255, points[i].color[2] / 255);
            // colors.push(color.r, color.g, color.b);

            // // Extract RGBA components
            // const r = points[i].color[0] / 255;
            // const g = points[i].color[1] / 255;
            // const b = points[i].color[2] / 255;
            // const a = points[i].color[3] / 255; // Alpha component

            // // Pre-multiply RGB components by alpha (straight alpha)
            // const premultipliedR = r * a;
            // const premultipliedG = g * a;
            // const premultipliedB = b * a;

            let alpha = points[i].color[3] / 255;
            let baseColor = new THREE.Color(
            points[i].color[0] / 255,
            points[i].color[1] / 255,
            points[i].color[2] / 255
            );

            // Modulate each component by alpha (assuming white background, hence 1 - alpha)
            colors.push(
            (1 - alpha) + alpha * baseColor.r,
            (1 - alpha) + alpha * baseColor.g,
            (1 - alpha) + alpha * baseColor.b
            );

            // Add positions and colors (with pre-multiplied alpha) to the arrays
            positions.push(...points[i].position);
            
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        
        const material = new THREE.PointsMaterial({ size: 0.03, vertexColors: true , transparent: true});
        const pointCloud = new THREE.Points(geometry,material);

        //translate/rotate/scale
        pointCloud.rotateX(2*Math.PI/3);
        pointCloud.scale.set(1, 1, 1);
        pointCloud.position.set(0, 1, 0);

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
