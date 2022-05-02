import { writable } from "svelte/store";
import type { User } from "./client";

export let user = writable<User>(null);
