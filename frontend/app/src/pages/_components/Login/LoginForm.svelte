<script>
    import { form, field } from 'svelte-forms';
    import { required } from 'svelte-forms/validators';
    import Textfield from '@smui/textfield';
    import Button, { Label } from '@smui/button';

    export let proccessAuthentication;

    const username = field('username', '', [required()]);
    const password = field('password', '', [required()]);
    const loginForm = form(username, password);

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            proccessAuthentication($loginForm, $username, $password);
        }
    };
</script>


<section on:keypress={handleKeyPress}>
    <Textfield
        class='login-input'
        type="text"
        variant="outlined"
        required={true}
        bind:value={$username.value} label="Username"
    />
    <Textfield 
        class='login-input'
        type="password"
        variant="outlined"
        required={true}
        bind:value={$password.value}
        label="Password"
    />

    <Button 
        class="login-button"
        variant="outlined"
        on:click={() => proccessAuthentication($loginForm, $username, $password)}
    >
        <Label>Login</Label>
    </Button>
</section>


<style>
    section{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }

    :global(.login-input){
        width: 80%;
        min-width: 300px;
    }

    :global(.login-button){
        width: 150px;
        height: 50px;
    }
</style>
