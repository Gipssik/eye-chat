import type { Form } from "svelte-forms/types";

export type IForm = {
    valid: boolean;
    dirty: boolean;
    readonly summary: {};
    errors: string[];
    hasError(this: Form, name: string): boolean;
};
