<script>
import { Course } from "@CourseBuilder/config/models"

// @component   PrimaryBreadcrumbs
// @info        currently only used to get back to the course list from a course detail/form page
export default {
    name: "PrimaryBreadcrumbs",
    inheritAttrs: false,
    computed: {
        count () { return this.routes.length },
        isSingle () {return this.count == 1 },
        routes () {
            return [
                {
                    label: this.$i18n.COURSES_VIEW,
                    href: this.$router.resolve({ name: "courseList" }).href, // @info    used to drive regular link
                    to: { name: "courseList" }, // @info    used to drive router link
                    useRoute: !!(Course.query().count() > 1) // @info    if we came here on an initial load, we'll only have one course, so we'll need to reload to get the full available course list
                }
            ]
        }
    },
    methods: {
        isBranch (index) { return !this.isLeaf(index) },
        isLeaf (index) { return (index === this.count - 1) },
    }
}
</script>

<template>
<nav
    class="breadcrumb flex:h--p:start--s:middle rhy:xStart25"
    v-if="count"
>
    <!-- single entity -->
    <template v-for="(route, index) in routes">
        <template v-if="route.useRoute">
            <router-link
                class="text-primary"
                :key="index"
                :to="route.to"
            >
                {{ route.label }}
            </router-link>
        </template>

        <template v-else>
            <a
                class="text-primary"
                :href="route.href"
                :key="index"
            >
                {{ route.label }}
            </a>
        </template>

        <template v-if="isBranch(index)">
            <span>/</span>
        </template>
    </template>
</nav>
</template>
