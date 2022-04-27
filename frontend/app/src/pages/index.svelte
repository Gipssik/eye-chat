<script>
    import { goto, metatags } from '@roxi/routify';
    import { user } from '../stores';
    
    metatags.description = 'A messanger for your eyes.';

    let currentUser;

    user.subscribe(u => {
        currentUser = u;
    })

    $: if(!currentUser) {
        $goto('./login');
    }
</script>

<h1>Welcome</h1>