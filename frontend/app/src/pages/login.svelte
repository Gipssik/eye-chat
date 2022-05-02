<script lang="ts">
    import { goto, metatags } from '@roxi/routify';
    import Button, { Label } from '@smui/button';
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
    import type { Field } from 'svelte-forms/types';
    import { LoginForm, BackgroundLogo } from './_components';
    import { user } from '../stores';
    import {
        AuthService,
        UsersService,
        type Body_login_access_token_api_auth_access_token_post as LoginData,
        type User
    } from '../client';
    import type { IForm } from '../types';

    metatags.title = 'EyeChat - Sign In';

    let modalTitle = '';
    let modalDescription = '';
    let modalOpened = false;

    let currentUser: User;
    user.subscribe((u: User) => {
        currentUser = u;
    })

    $: if(currentUser) {
        $goto('/');
    }

    const authenticate = async (username: Field<string>, password: Field<string>) => {
        let data: LoginData = {
            username: username.value,
            password: password.value
        }

        const token = await AuthService.loginAccessTokenApiAuthAccessTokenPost(data);
        localStorage.setItem('access_token', token.access_token);
        const me = await UsersService.getUserMeApiUsersMeGet();
        user.set(me);
    };

    const processAuthentication = (
        loginForm: IForm,
        username: Field<string>,
        password: Field<string>
    ) => {
        if (loginForm.dirty && loginForm.valid){
            authenticate(username, password)
                .catch(err => {
                    modalTitle = 'Credentials Error';
                    modalDescription = 'Username or password are invalid';
                    modalOpened = true;
                });
        }
    };
</script>


<Dialog bind:open={modalOpened}>
    <Title>{modalTitle}</Title>
    <Content>{modalDescription}</Content>
    <Actions>
        <Button on:click={() => {modalOpened = false}}>
            <Label>OK</Label>
        </Button>
    </Actions>
</Dialog>
<div class="form-container">

    <BackgroundLogo/>

    <div>
        <h1>Sign in</h1>
        <LoginForm {processAuthentication}/>
    </div>
</div>
