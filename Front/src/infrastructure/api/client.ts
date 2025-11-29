import axios from 'axios';
import type { OptimizationResult } from '../../domain/models/types';

const API_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'multipart/form-data',
    },
});

export interface OptimizeParams {
    file?: File;
    n_clusters: number;
    method: string;
    use_csv: boolean;
    date_filter?: string;
    manual_points?: { lat: number; lng: number; name: string }[];
    max_points: number;
}

export const optimizeRoute = async (params: OptimizeParams): Promise<OptimizationResult> => {
    const formData = new FormData();

    if (params.file) {
        formData.append('file', params.file);
    }

    formData.append('n_clusters', params.n_clusters.toString());
    formData.append('method', params.method);
    formData.append('use_csv', params.use_csv.toString());
    formData.append('max_points', params.max_points.toString());

    if (params.date_filter) {
        formData.append('date_filter', params.date_filter);
    }

    if (params.manual_points) {
        formData.append('manual_points_json', JSON.stringify(params.manual_points));
    }

    const response = await apiClient.post<OptimizationResult>('/optimize', formData);
    return response.data;
};
