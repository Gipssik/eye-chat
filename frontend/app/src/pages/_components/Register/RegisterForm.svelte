<script lang="ts">
    import { goto } from "@roxi/routify";
    import Button, { Label } from "@smui/button";
    import Textfield from "@smui/textfield";
    import { field, form } from "svelte-forms";
    import type { Field } from "svelte-forms/types";
    import { email as emailValidator, min, pattern, required } from "svelte-forms/validators";
    import type { IForm } from "../../../types";

    export let processRegistration: (
        registerForm: IForm,
        username: Field<string>,
        email: Field<string>,
        password: Field<string>
    ) => void;
    export let validationErrors = [] as string[];

    const username = field("username", "", [required(), min(4), pattern(/^[a-zA-Z0-9_]+$/)]);
    const email = field("email", "", [required(), emailValidator()]);
    const password = field("password", "", [required(), min(8)]);
    const registerForm = form(username, email, password);

    const callProcessing = () => {
        processRegistration($registerForm, $username, $email, $password);
    }

    const handleKeyPress = (e: KeyboardEvent) => {
        if (e.key === 'Enter') {
            callProcessing();
        }
    };
</script>

<section on:keypress={handleKeyPress}>
    <Textfield
        class='form-input'
        type="text"
        variant="outlined"
        required={true}
        bind:value={$username.value} label="Username"
    />
    <Textfield
        class='form-input'
        type="text"
        variant="outlined"
        required={true}
        bind:value={$email.value} label="Email"
    />
    <Textfield
        class='form-input'
        type="password"
        variant="outlined"
        required={true}
        bind:value={$password.value}
        label="Password"
    />

    {#if validationErrors.length > 0}
        <div class="error-block">
            {#each validationErrors as error (error)}
                <span class="error">{error}</span>
            {/each}
        </div>
    {/if}

    <div class="bottom-block">
        <Button
            class="form-button"
            variant="outlined"
            on:click={callProcessing}
        >
            <Label>Register</Label>
        </Button>
        <sub>Already have an account? Sign in <span on:click={() => $goto("/login")}>here</span></sub>
    </div>

</section>

<style>
    .error-block{
        display: flex;
        flex-direction: column;
        width: 80%;
        min-width: 300px;
        background-color: #a00000;
        padding: 5px 10px;
        border-radius: 5px;
    }

    .error {
        color: #fff;
        font-size: 14px;
        margin: 0;
    }

    .error::before {
        content: '• ';
    }
</style>
