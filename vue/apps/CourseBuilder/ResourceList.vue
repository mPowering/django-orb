<script>
import Draggable from "vuedraggable"

export default {
    name: "ResourceList",
    components: {
        Draggable,
    },
    props: {
        // @prop    resources
        // @desc    list of currently search resource files
        resources: {
            type: Array,
            default: () => ([])
        }
    },
    data () {
        return {
            // @prop    dragOptions
            // @desc    passed options to Vue Draggable
            // @info    group name of "resources" will help enact drop
            dragOptions: {
                handle: ".handle",
                group: {
                    name: "resources",
                    pull: "clone",
                    put: false
                }
            }
        }
    },
    computed: {
        processedResources () {
            return this.resources
                .reduce(
                    (resourceList, { title, files }) => {
                        files = files.flatMap(
                            ({ file_extension, ...attrs }) => ({
                                ...attrs,
                                fileExtension: file_extension,
                                parentTitle: title,
                                type: "CourseResource"
                            })
                        ).filter( file => file.is_embeddable )

                        return resourceList.concat(files)
                    },
                    []
                )
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
<draggable
    class="resource-list"
    :list="processedResources"
    :options="dragOptions"
>
    <div class="list-group-item flex:h--p:start--s:base rhy:xStart25 pad:xyEq25 rxn:info"
        v-for="instance in processedResources"
        :key="instance.id"
    >
        <span
            class="handle glyph pad:x25 pad:y0 "
            role="button"
        >
            <img src="/static/orb/images/glyphicons-move.png" />
        </span>

        <div>{{ instance | niceTitle }}</div>
    </div>
</draggable>
</template>


<style>
.resource-list .handle { cursor: grab }
.resource-list .handle img {
    height: 16px;
    margin-top: -5px;
    width: 16px
}
</style>
