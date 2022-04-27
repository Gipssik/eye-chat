<script>
  import { onMount } from "svelte";
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  import { instance } from "./Instance"
  import { user } from "./stores";

  onMount(() => {
    instance.get('users/me')
    .then(response => {
      user.set(response.data);
    })
    .catch(error => {
      user.set(null);
    });
  })
</script>

<Router {routes} />