/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { UserUpdate } from '../models/UserUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * Get Users
     * Get list of users.
     *
     * Args:
     * skip (Optional[int], optional): Number of users to skip. Defaults to 0.
     * limit (Optional[int], optional): Max amount of users to return. Defaults to 100.
     * user_dao (UserDAO, optional): User DAO.
     *
     * Returns:
     * list[User]: List of users.
     * @param skip
     * @param limit
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getUsersApiUsersGet(
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<Array<User>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create User
     * Create new user.
     *
     * Args:
     * user (schema.UserCreate): User data.
     * user_dao (UserDAO, optional): User DAO.
     *
     * Raises:
     * HTTPException: User already exists.
     *
     * Returns:
     * User: User.
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static createUserApiUsersPost(
        requestBody: UserCreate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Me
     * Get current user.
     *
     * Args:
     * current_user (User, optional): Current user.
     *
     * Returns:
     * User: Current user.
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getUserMeApiUsersMeGet(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/me',
        });
    }

    /**
     * Get User
     * Get user by id.
     *
     * Args:
     * user_id (UUID): User ID.
     * user_dao (UserDAO, optional): User DAO.
     *
     * Raises:
     * UserNotFoundException: User not found.
     *
     * Returns:
     * User: User.
     * @param userId
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getUserApiUsersUserIdGet(
        userId: string,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete User
     * Delete user.
     *
     * Args:
     * user_id (UUID): User ID.
     * user_dao (UserDAO, optional): User DAO.
     * current_user (User, optional): Current user.
     *
     * Raises:
     * HTTPException: You are not allowed to delete this user.
     * HTTPException: User not found.
     * @param userId
     * @returns void
     * @throws ApiError
     */
    public static deleteUserApiUsersUserIdDelete(
        userId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User
     * Update user.
     *
     * Args:
     * user_id (UUID): User ID.
     * user (schema.UserUpdate): User data.
     * user_dao (UserDAO, optional): User DAO.
     * current_user (User, optional): Current user.
     *
     * Raises:
     * HTTPException: You are not allowed to update this user.
     * HTTPException: User not found.
     * HTTPException: Username or email already exists.
     *
     * Returns:
     * User: User.
     * @param userId
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static updateUserApiUsersUserIdPatch(
        userId: string,
        requestBody: UserUpdate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
