/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MonitoringService {

    /**
     * Health Check
     * Checks the health of a project.
     *
     * It returns 200 if the project is healthy.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static healthCheckApiHealthGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/health',
        });
    }

}
