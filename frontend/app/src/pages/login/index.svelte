<script>
    import { goto } from '@roxi/routify';
    import Button, { Label } from '@smui/button';
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
    import { LoginForm } from '../_components/Login';
    import { user } from '../../stores';
    import { getAccessToken, setupUser } from '../../api/user';


    let modalTitle = '';
    let modalDescription = '';
    let modalOpened = false;

    let currentUser;
    user.subscribe(u => {
        currentUser = u;
    })

    $: if(currentUser) {
        $goto('/');
    }

    const authenticate = async (username, password) => {
        let data = new URLSearchParams();
        data.append('username', username.value);
        data.append('password', password.value);

        const token=await getAccessToken(data);
        localStorage.setItem('access_token',token);
        setupUser(user);

        $goto('/');
    };

    const proccessAuthentication = (loginForm, username, password) => {
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


<div class="container">
    <Dialog bind:open={modalOpened}>
        <Title>{modalTitle}</Title>
        <Content>{modalDescription}</Content>
        <Actions>
            <Button on:click={() => {modalOpened = false}}>
                <Label>OK</Label>
            </Button>
        </Actions>
    </Dialog>

    <span class="background-title">
        <span>Eye</span>Chat
    </span>

    <div>
        <h1>Sign in</h1>
        <LoginForm {proccessAuthentication}/>
    </div>
</div>


<style>
    .container{
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
    }

    .container > div{
        height: fit-content;
        width: 25vw;
        min-width: 350px;
        background-color: #2f8b62;
        border-radius: 5px;
        padding: 50px 10px;
        z-index: 1;
        mask-image: linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0.95));
        mask-size: 100%;
        mask-repeat: no-repeat;
        -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0.95));
        -webkit-mask-size: 100%;
        -webkit-mask-repeat: no-repeat;
    }

    .container h1{
        color: #fff;
        text-align: center;
        font-size: 35px;
    }

    .background-title{
        position: absolute;
        font-size: 22rem;
        top: 10px;
    }

    .background-title span{
        color: #48bf84;
        font-weight: bold;
    }

</style>