<script lang="ts">
    import { form, field } from 'svelte-forms';
    import { required } from 'svelte-forms/validators';
    import Textfield from '@smui/textfield';
    import Button, { Label } from '@smui/button';
    import type { Field } from 'svelte-forms/types';
    import type { IForm } from '../../../types';
    import { goto } from '@roxi/routify';

    export let processAuthentication: (
        loginForm: IForm,
        username: Field<string>,
        password: Field<string>
    ) => void;

    const username = field('username', '', [required()]);
    const password = field('password', '', [required()]);
    const loginForm = form(username, password);

    const callProcessing = () => {
        processAuthentication($loginForm, $username, $password);
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
        type="password"
        variant="outlined"
        required={true}
        bind:value={$password.value}
        label="Password"
    />

    <div class="bottom-block">
        <Button
            class="form-button"
            variant="outlined"
            on:click={callProcessing}
        >
            <Label>Login</Label>
        </Button>
        <sub>Don't have an account? Sign up <span on:click={() => $goto("/register")}>here</span></sub>
    </div>

</section>
