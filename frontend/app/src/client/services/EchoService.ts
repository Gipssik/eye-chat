/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Message } from '../models/Message';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class EchoService {

    /**
     * Send Echo Message
     * Send echo back to user.
     *
     * :param incoming_message: incoming message.
     * :returns: message same as the incoming.
     * @param requestBody
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static sendEchoMessageApiEchoPost(
        requestBody: Message,
    ): CancelablePromise<Message> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/echo',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
