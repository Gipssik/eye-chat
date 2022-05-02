/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * DTO model for User from db for output.
 */
export type User = {
    username: string;
    email: string;
    id: string;
    first_name?: string;
    last_name?: string;
    is_superuser: boolean;
    is_active: boolean;
    is_reported: boolean;
    is_blocked: boolean;
    preferences?: string;
    created_at: string;
    updated_at: string;
};
