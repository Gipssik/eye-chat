<script lang="ts">
    import { onMount } from "svelte";
    import { metatags, Router } from "@roxi/routify";
    import { routes } from "../.routify/routes";
    import { user } from "./stores";
    import { UsersService } from "./client";

    metatags.description = 'A messanger for your eyes.';

    onMount(() => {
        UsersService.getUserMeApiUsersMeGet()
            .then(response => {
                user.set(response);
            })
            .catch(error => {
                user.set(null);
            });
    })
</script>

<Router {routes} />
