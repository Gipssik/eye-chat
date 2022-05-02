<script lang="ts">
    import { goto, metatags } from "@roxi/routify";
    import Button, { Label } from "@smui/button";
    import Dialog, { Actions, Content, Title } from "@smui/dialog";
    import type { Field } from "svelte-forms/types";
    import { UsersService, type User, type UserCreate } from "../client";
    import { user } from "../stores";
    import type { IForm } from "../types";
    import { BackgroundLogo, RegisterForm } from "./_components";

    metatags.title = "EyeChat - Sign Up";

    let modalTitle = '';
    let modalDescription = '';
    let modalOpened = false;

    let validationErrors = [] as string[];
    const errors = {
        username: {
            min: "Username must be at least 4 characters long",
            pattern: "Username can only contain letters, numbers and underscores",
        },
        email: {
            not_an_email: "Email is not valid",
        },
        password: {
            min: "Password must be at least 8 characters long",
        },
    }

    let currentUser: User;
    user.subscribe((u: User) => {
        currentUser = u;
    })

    $: if(currentUser) {
        $goto('/');
    }

    const register = async (
        username: string,
        email: string,
        password: string
    ) => {
        const data: UserCreate = {
            username,
            email,
            password
        };

        const user = await UsersService.createUserApiUsersPost(data)
        $goto('/login');
    };

    const processValidation = (field: Field<string>) => {
        if (!field.valid) {
            for(let title of Object.keys(errors[field.name])){
                if(field.errors.includes(title) && !validationErrors.includes(errors[field.name][title])){
                    validationErrors = [...validationErrors, errors[field.name][title]];
                }else if(!field.errors.includes(title)){
                    validationErrors = validationErrors.filter(e => e !== errors[field.name][title]);
                }
            }
        } else {
            validationErrors = validationErrors.filter(e => !Object.values(errors[field.name]).includes(e));
        }
    }

    const processRegistration = (
        registerForm: IForm,
        username: Field<string>,
        email: Field<string>,
        password: Field<string>
    ) => {
        for (const field of [username, email, password]) {
            processValidation(field);
        }

        if (validationErrors.length === 0 && registerForm.dirty && registerForm.valid){
            register(username.value, email.value, password.value)
                .catch(err => {
                    modalTitle = 'Registration Error';
                    modalDescription = 'Username or email already exists';
                    modalOpened = true;
                });
        }
    }
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
        <h1>Sign Up</h1>
        <RegisterForm {processRegistration} {validationErrors}/>
    </div>
</div>
