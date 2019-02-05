<script>
export default {
    name: "CourseResource",
    props: {
        instance: {
            type: Object,
            default: () => ({
                title: this.$i18n.RESOURCE_TITLE_NEW,
            })
        },
    },
    data () {
        return {
            resource: {
                ...this.instance
            },
        }
    },
    filters: {
        niceTitle (instance) {
            let title = `(${ instance.fileExtension })` || ""

            title = instance.title
                ? `${ instance.title } ${ title }`
                : title

            title = instance.parentTitle
                ? `${ title } - ${ instance.parentTitle } `
                : title

            return title
        }
    },
}
</script>

<template>
<div class="course-resource panel panel-success edge:xyEq">
    <header
        class="course-resource-hdr panel-heading flex:h--p:start--s:middle rhy:xStart25"
    >
        <slot name="entry:preheading"></slot>

        <h5>{{ resource | niceTitle }}</h5>

        <slot name="entry:postheading"></slot>
    </header>

    <div
        class="panel-body"
        v-if="resource.tags"
    >
        <span
            class="label label-info pull-left iso:xEnd25 iso:yEnd25"
            v-for="tag in resource.tags"
            :key="tag.id"
        >
            {{ tag.tag.name }}
        </span>
    </div>
</div>
</template>
