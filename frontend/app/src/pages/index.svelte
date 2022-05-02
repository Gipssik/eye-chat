<script lang="ts">
    import { goto, metatags } from '@roxi/routify';
    import Button, { Label } from '@smui/button';
    import type { User } from '../client';
    import { user } from '../stores';

    metatags.title = 'EyeChat - Messages';

    let currentUser: User;

    user.subscribe((u: User) => {
        currentUser = u;
    })

    $: if(!currentUser) {
        $goto('/login');
    }

    const logout = () => {
        localStorage.removeItem('access_token');
        user.set(null);
    }
</script>

<h1>Welcome</h1>
<Button color="secondary" on:click={logout} variant="outlined">
    <Label>Log out</Label>
</Button>
