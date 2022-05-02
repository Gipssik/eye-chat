/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RedisValueDTO } from '../models/RedisValueDTO';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RedisService {

    /**
     * Get Redis Value
     * Get value from redis.
     *
     * :param key: redis key, to get data from.
     * :param redis: redis connection.
     * :returns: information from redis.
     * @param key
     * @returns RedisValueDTO Successful Response
     * @throws ApiError
     */
    public static getRedisValueApiRedisGet(
        key: string,
    ): CancelablePromise<RedisValueDTO> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/redis/',
            query: {
                'key': key,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Set Redis Value
     * Set value in redis.
     *
     * :param redis_value: new value data.
     * :param redis: redis connection.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static setRedisValueApiRedisPut(
        requestBody: RedisValueDTO,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/redis/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
