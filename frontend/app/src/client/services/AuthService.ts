/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_access_token_api_auth_access_token_post } from '../models/Body_login_access_token_api_auth_access_token_post';
import type { Token } from '../models/Token';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AuthService {

    /**
     * Login Access Token
     * Returns access token if valid username and password are provided.
     *
     * Args:
     * user_dao (UserDAO): User DAO.
     * form_data (OAuth2PasswordRequestForm): User credentials.
     *
     * Raises:
     * HTTPException: User not found or password is invalid.
     * HTTPException: User is not active.
     * @param formData
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginAccessTokenApiAuthAccessTokenPost(
        formData: Body_login_access_token_api_auth_access_token_post,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/access-token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Token Test
     * Returns current user if valid access token is provided
     *
     * Args:
     * current_user (User): Current user.
     *
     * Returns:
     * User: Current user.
     * @returns User Successful Response
     * @throws ApiError
     */
    public static tokenTestApiAuthTestTokenPost(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/test-token',
        });
    }

}
