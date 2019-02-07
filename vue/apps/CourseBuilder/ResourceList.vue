<script>
import { api } from "@services/api"
import API_ROUTES from "@CourseBuilder/config/apiRoutes"

import Draggable from "vuedraggable"
import SearchField from "@fields/SearchField"


export default {
    name: "ResourceList",
    components: {
        Draggable,
        SearchField
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
            },

            // @prop    q
            // @desc    query string for searching server db for applicable resources
            q: "",

            // @prop    availableResources
            // @desc    list of queried resource results from a search
            resources: [],
        }
    },
    computed: {
        // @prop    processedResources
        // @desc    map returned resources with extra data information for processing
        // @        filter out those items that are not considered embeddable by the server
        processedResources () {
            return this.resources
                .reduce(
                    (resourceList, { title, files }) => {
                        files = files
                            .map(
                                ({ file_extension, ...attrs }) => ({
                                    ...attrs,
                                    fileExtension: file_extension,
                                    parentTitle: title,
                                    type: "CourseResource"
                                })
                            )
                        files = [].concat(...files)
                            .filter( file => file.is_embeddable )

                        return resourceList.concat(files)
                    },
                    []
                )
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
    methods: {
        // @func    searchResources
        // @desc    request a queried set of resources from server
        // @        and assign to available resources
        async searchResources () {
            try {
                let { objects: resources } = await api
                    .fetch({
                        route: API_ROUTES.RESOURCE_SEARCH,
                        params: {
                            format: "json",
                            q: this.q
                        }
                    })

                this.resources = resources
            }
            catch (error) { console.log(error) }

            return
        },
    }
}
</script>


<template>
<div>
    <search-field
        v-model="q"
        @submit="searchResources"
    >
        {{ $i18n.RESOURCE_LABEL_SEARCH }}
    </search-field>

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
</div>
</template>
