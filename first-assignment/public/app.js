//TODO: try to figure out orbitControl dependencies
async function fetchAndParsePoints() {
    // Getting points from the splat and storing them into a point array with information about them
    const response = await fetch('plush.splat'); //set different parameters for scaling based on the name of the file
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

function sortPoints(points, camera_x,camera_y,camera_z){
    points.sort((a, b) => { //sort from max to min distance to the camera
        const distanceA = calculateDistance(a, camera_x, camera_y, camera_z);
        const distanceB = calculateDistance(b, camera_x, camera_y, camera_z);
        return distanceB - distanceA;
    });

    return points;

}

function gaussianFalloff(distance, sigma) {
    // Calculate the Gaussian falloff factor
    const exponent = -0.5 * (distance / sigma) ** 2;
    return Math.exp(exponent);
}

//fucntion for initailizing the scene, camera, pointcloud, setting the colors of the splats
function init3DScene(points, sigma) {

    console.log("rendering")
        const camera_x = 0; // nike : 5, plush: 5 , train : 0
        const camera_y = 0; // nike : 0, plush: 0  , train : 0
        const camera_z = 5;  // nike : 0, plush: 0  , train :  5      

        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff); // set to white
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000); //human eye perspective
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // Adjust camera position based on the splat
        camera.position.set(camera_x,camera_y,camera_z)

        const center = new THREE.Vector3();
        const falloffFactors = points.map((point) => {
        const distance = new THREE.Vector3().fromArray(point.position).distanceTo(center);
        return gaussianFalloff(distance, sigma);
        });

       sortPoints(points,camera_x,camera_y,camera_z);

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

        const backColor = new THREE.Color();
        backColor.setRGB(1 ,1, 1);

      console.log(points[0].color[3])
      console.log(points[1].color[3])
      console.log(points[2].color[3])
       for(let i = 0; i < points.length; i++) {
           positions.push(...points[i].position);
            // //TODO: implement alpha blending
            const color = new THREE.Color();
            color.setRGB(points[i].color[0] / 255, points[i].color[1] / 255, points[i].color[2] / 255);
            //const alpha = falloffFactors[i];
            colors.push(color.r, color.g, color.b);
            //colors.push(alpha);


            // // //color and alpha of the point
            // let alpha = points[i].color[3] / 255;
            // let baseColor = new THREE.Color();
            // baseColor.setRGB(
            // points[i].color[0] / 255,
            // points[i].color[1] / 255,
            // points[i].color[2] / 255
            // );
    
            // //Modulate each component by alpha (assuming white background, hence 1 - alpha)
            // colors.push(
            // (1 - alpha)*backColor.r + alpha * baseColor.r,
            // (1 - alpha)*backColor.g + alpha * baseColor.g,
            // (1 - alpha)*backColor.b + alpha * baseColor.b
            // );
            
        }
        console.log(colors[1].a)

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        
        const material = new THREE.PointsMaterial({ size: 0.03, vertexColors: true , transparent: true});

        material.blending = THREE.CustomBlending;
        material.blendSrc = THREE.SrcAlphaFactor;
        material.blendDst = THREE.OneMinusSrcAlphaFactor;
        material.blendEquation = THREE.AddEquation;


        const pointCloud = new THREE.Points(geometry,material);

        //translate/rotate/scale
        pointCloud.rotateX(3*Math.PI/4); // nike : 2*Math.PI/3, plush: 3*Math.PI/4) , train : Math.PI
        //pointCloud.rotateY(Math.PI); //only for train 
        pointCloud.scale.set(1.2, 1.2, 1.2);    // nike : 1,1,1, plush: 1.2, 1.2, 1.2, train :  1,1,1
        pointCloud.position.set( 0,1,0);  // nike : 0,1,0 plush: 0,1,0 , train : 0,0,0
      

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

function updatePointsGauss(scene, sigma){
  //TODO

}


async function loadAndInitScene() {
    //scaling factor 
    const def_scaling_factor = 1.0; //default value before user input
    let scaling_factor = def_scaling_factor;
    const scalingSlider = document.getElementById('scaling-slider');

    //listeners for parameter changes
    try {
        let sigma = 3.0;
        const points = await fetchAndParsePoints();
        console.log("Points saved")
        scene = init3DScene(points, sigma);

         // Update scaling factor when the slider value changes
        scalingSlider.addEventListener('input', () => {
        scaling_factor = parseFloat(scalingSlider.value);
    
        updatePointsGeometry(scene, scaling_factor);
        });

        sigmaSlider.addEventListener('input', () => {
            sigma = parseFloat(sigmaSlider.value);
        ;
            updatePointsGauss(scene, sigma);
        });
    } catch (error) {
        console.error("Failed to load or initialize the scene:", error);
    }

}

// Function that loads points and initializes the scene.
loadAndInitScene();
