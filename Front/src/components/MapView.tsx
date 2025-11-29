import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import type { Cluster } from '../domain/models/types';

// Fix Leaflet icon issue
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

interface MapViewProps {
    routeCoords: number[][];
    clusters: Cluster[];
    manualPoints: { lat: number; lng: number; name: string }[];
    onMapClick?: (lat: number, lng: number) => void;
    isManualMode: boolean;
}

const MapEvents = ({ onMapClick, isManualMode }: { onMapClick?: (lat: number, lng: number) => void, isManualMode: boolean }) => {
    useMapEvents({
        click(e: L.LeafletMouseEvent) {
            if (isManualMode && onMapClick) {
                onMapClick(e.latlng.lat, e.latlng.lng);
            }
        },
    });
    return null;
};

const FitBounds = ({ coords }: { coords: number[][] }) => {
    const map = useMap();
    useEffect(() => {
        if (coords.length > 0) {
            const bounds = L.latLngBounds(coords.map(c => [c[0], c[1]]));
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }, [coords, map]);
    return null;
};

// Function to create a colored dot icon
const createClusterIcon = (color: string) => {
    return L.divIcon({
        className: 'custom-cluster-icon',
        html: `<div style="
            background-color: ${color};
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 0 4px rgba(0,0,0,0.5);
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
    });
};

// Function to create a red dot icon for manual points
const createManualIcon = () => {
    return L.divIcon({
        className: 'custom-manual-icon',
        html: `<div style="
            background-color: #ef4444;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 0 4px rgba(0,0,0,0.5);
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
    });
};

export const MapView: React.FC<MapViewProps> = ({ routeCoords, clusters, manualPoints, onMapClick, isManualMode }) => {
    const center = [-12.0464, -77.0428]; // Lima

    // State for mixed route segments (Road vs Direct/Sea)
    interface RouteSegment {
        coords: number[][];
        type: 'road' | 'direct';
    }
    const [routeSegments, setRouteSegments] = useState<RouteSegment[]>([]);

    // Calculate bounds to fit everything
    const allCoords = [
        ...routeCoords,
        ...clusters.flatMap(c => c.coords)
    ];

    const boundsCoords = allCoords.length > 0 ? allCoords : (manualPoints.length > 0 ? manualPoints.map(p => [p.lat, p.lng]) : []);

    // Fetch OSRM Route with Chunking & Style Fallback
    useEffect(() => {
        const fetchRoute = async () => {
            if (routeCoords.length < 2) {
                setRouteSegments([]);
                return;
            }

            // Reduce chunk size to improve OSRM reliability for long distances
            const CHUNK_SIZE = 10;
            const chunks = [];

            for (let i = 0; i < routeCoords.length - 1; i += CHUNK_SIZE - 1) {
                const chunk = routeCoords.slice(i, i + CHUNK_SIZE);
                if (chunk.length >= 2) {
                    chunks.push(chunk);
                }
            }

            const newSegments: RouteSegment[] = [];

            // Fetch sequentially to avoid OSRM Demo Server rate limiting (HTTP 429)
            for (const chunk of chunks) {
                const coordinates = chunk.map(c => `${c[1]},${c[0]}`).join(';');
                try {
                    const response = await fetch(`https://router.project-osrm.org/route/v1/driving/${coordinates}?overview=full&geometries=geojson`);
                    if (!response.ok) throw new Error('OSRM Error');
                    const data = await response.json();
                    if (data.routes && data.routes.length > 0) {
                        newSegments.push({
                            coords: data.routes[0].geometry.coordinates.map((c: number[]) => [c[1], c[0]]),
                            type: 'road'
                        });
                        continue; // Success, move to next chunk
                    }
                } catch (e) {
                    // Silent fail
                }

                // Fallback: Direct line
                newSegments.push({
                    coords: chunk,
                    type: 'direct'
                });

                // Small delay to be nice to the server
                await new Promise(resolve => setTimeout(resolve, 100));
            }

            setRouteSegments(newSegments);
        };

        fetchRoute();
    }, [routeCoords]);

    return (
        <MapContainer center={center as L.LatLngExpression} zoom={12} style={{ height: '100%', width: '100%', background: '#0a0b0d' }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            <MapEvents onMapClick={onMapClick} isManualMode={isManualMode} />
            {boundsCoords.length > 0 && <FitBounds coords={boundsCoords as number[][]} />}

            {/* Clusters with Colored Icons */}
            {clusters.map((cluster) => (
                <React.Fragment key={cluster.id}>
                    {cluster.coords.map((coord, idx) => (
                        <Marker
                            key={`${cluster.id}-${idx}`}
                            position={coord as L.LatLngExpression}
                            icon={createClusterIcon(cluster.color)}
                        >
                            <Popup>
                                <div className="text-xs font-bold">{cluster.names[idx]}</div>
                                <div className="text-[10px] text-gray-500">Cluster: {cluster.id}</div>
                            </Popup>
                        </Marker>
                    ))}
                </React.Fragment>
            ))}

            {/* Manual Points */}
            {manualPoints.map((point, idx) => (
                <Marker
                    key={`manual-${idx}`}
                    position={[point.lat, point.lng] as L.LatLngExpression}
                    icon={createManualIcon()}
                >
                    <Popup>{point.name}</Popup>
                </Marker>
            ))}

            {/* Render Route Segments (Only Roads) */}
            {routeSegments.map((segment, idx) => {
                // User requested to remove dashed lines completely to avoid visual clutter
                if (segment.type !== 'road') return null;

                return (
                    <Polyline
                        key={`route-${idx}`}
                        positions={segment.coords as L.LatLngExpression[]}
                        pathOptions={{ color: '#3b82f6', weight: 4, opacity: 0.8 }} // Blue Solid (Road)
                    />
                );
            })}
        </MapContainer>
    );
};
