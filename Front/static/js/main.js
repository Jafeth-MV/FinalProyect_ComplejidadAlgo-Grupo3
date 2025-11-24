document.addEventListener('DOMContentLoaded', () => {
    // Initialize Map
    const map = L.map('map').setView([-12.0464, -77.0428], 13); // Lima default

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // State
    let currentMarkers = [];
    let currentRouteControl = null;
    let clusterLayers = [];

    // UI Elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const panels = document.querySelectorAll('.panel');
    const optimizeBtn = document.getElementById('optimize-btn');
    const loader = optimizeBtn.querySelector('.loader');
    const btnText = optimizeBtn.querySelector('.btn-text');
    const statsPanel = document.getElementById('stats-panel');
    const fileInput = document.getElementById('excel-file');
    const fileLabel = fileInput.nextElementSibling.querySelector('.text');
    const nClustersInput = document.getElementById('n-clusters');
    const clusterValue = document.getElementById('cluster-value');

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}-panel`).classList.add('active');
        });
    });

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileLabel.textContent = e.target.files[0].name;
        }
    });

    // Cluster Slider
    nClustersInput.addEventListener('input', (e) => {
        clusterValue.textContent = e.target.value;
    });

    // Optimize Button Click
    optimizeBtn.addEventListener('click', async () => {
        const mode = document.querySelector('.tab-btn.active').dataset.tab;
        const formData = new FormData();

        formData.append('n_clusters', nClustersInput.value);

        if (mode === 'upload') {
            if (!fileInput.files[0]) {
                alert('Por favor selecciona un archivo Excel');
                return;
            }
            formData.append('file', fileInput.files[0]);
        } else {
            formData.append('use_random', 'true');
            formData.append('n_points', document.getElementById('n-points').value);
        }

        setLoading(true);

        try {
            const response = await fetch('/api/optimize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            visualizeResults(data);

        } catch (error) {
            console.error('Error:', error);
            alert('Error al optimizar: ' + error.message);
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        optimizeBtn.disabled = isLoading;
        if (isLoading) {
            loader.classList.remove('hidden');
            btnText.textContent = 'Procesando...';
        } else {
            loader.classList.add('hidden');
            btnText.textContent = 'Optimizar Ruta';
        }
    }

    function visualizeResults(data) {
        // Clear previous
        clearMap();

        // Show Stats
        statsPanel.classList.remove('hidden');
        document.getElementById('total-dist').textContent = `${data.stats.total_distance.toFixed(2)} km`;
        document.getElementById('exec-time').textContent = `${data.stats.execution_time.toFixed(3)} s`;

        const routeList = document.getElementById('route-list');
        routeList.innerHTML = '';
        data.route_names.forEach(name => {
            const li = document.createElement('li');
            li.textContent = name;
            routeList.appendChild(li);
        });

        // Draw Clusters (Markers)
        const colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#6366f1', '#14b8a6', '#f97316', '#84cc16'];

        data.clusters.forEach((cluster, index) => {
            const color = colors[index % colors.length];
            
            cluster.coords.forEach(coord => {
                const marker = L.circleMarker(coord, {
                    radius: 8,
                    fillColor: color,
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).bindPopup(`Cluster ${cluster.id}`);
                
                marker.addTo(map);
                currentMarkers.push(marker);
            });
        });

        // Draw Route using OSRM (Leaflet Routing Machine)
        // We need to pass waypoints. LRM might be slow for many points, 
        // so we might need to just draw lines if too many, but user asked for streets.
        // Let's try LRM but with a trick: we only pass the ordered waypoints.
        
        const waypoints = data.route_coords.map(c => L.latLng(c[0], c[1]));

        // If too many points, OSRM might reject or be slow. 
        // Free OSRM demo server has limits.
        // If > 25 points, maybe just draw polylines to be safe, or batch it?
        // For now, let's try to route them all.
        
        if (currentRouteControl) {
            map.removeControl(currentRouteControl);
        }

        currentRouteControl = L.Routing.control({
            waypoints: waypoints,
            router: L.Routing.osrmv1({
                serviceUrl: 'https://router.project-osrm.org/route/v1'
            }),
            lineOptions: {
                styles: [{color: '#3b82f6', opacity: 0.8, weight: 5}]
            },
            createMarker: function() { return null; }, // We already added colored markers
            addWaypoints: false,
            draggableWaypoints: false,
            fitSelectedRoutes: true,
            show: false // Don't show the itinerary container
        }).addTo(map);

        // Fit bounds
        const bounds = L.latLngBounds(data.route_coords);
        map.fitBounds(bounds, { padding: [50, 50] });
    }

    function clearMap() {
        currentMarkers.forEach(m => map.removeLayer(m));
        currentMarkers = [];
        if (currentRouteControl) {
            map.removeControl(currentRouteControl);
            currentRouteControl = null;
        }
    }
});
