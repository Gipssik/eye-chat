/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * DTO model for updating an existing user.
 */
export type UserUpdate = {
    username?: string;
    email?: string;
    password?: string;
    first_name?: string;
    last_name?: string;
    is_superuser?: boolean;
    is_active?: boolean;
    is_reported?: boolean;
    is_blocked?: boolean;
    preferences?: string;
};
