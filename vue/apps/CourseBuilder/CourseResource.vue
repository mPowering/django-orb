<script>
export default {
    name: "CourseResource",
    props: {
        // @prop    instance
        // @desc    individual resource instance assigned to a course section
        instance: {
            type: Object,
            default: () => ({
                title: this.$i18n.RESOURCE_TITLE_NEW,
            })
        },
    },
    data () {
        return {
            // @prop    resource
            // @data    local representation of instance that can be overloaded
            resource: {
                ...this.instance
            },
        }
    },
    filters: {
        // @filter  niceTitle
        // @desc    define the instance's visible title programmatically
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
<div class="course-resource panel panel-success iso:yEnd0 edge:xyEq">
    <header
        class="course-resource-hdr panel-heading flex:h--p:start--s:middle pad:xyEq25 rhy:xStart25"
    >
        <slot name="preheading"></slot>

        <h5 class="iso:yEnd0">{{ resource | niceTitle }}</h5>

        <slot name="postheading"></slot>
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
