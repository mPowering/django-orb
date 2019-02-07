<script>
import { generateUUID } from "@utils/uuid"

import Draggable from "vuedraggable"

import CourseActivity from "@CourseBuilder/CourseActivity"
import CourseResource from "@CourseBuilder/CourseResource"


export const defaultSectionSchema = { resources: [] }

export default {
    name: "CourseSection",
    components: {
        CourseActivity,
        CourseResource,
        Draggable
    },
    props: {
        // @prop    instance
        // @desc    individual section instance assigned to a course
        instance: {
            type: Object,
            default: () => ({})
        }
    },
    data () {
        return {
            // @prop    currentResources
            // @desc    initiate local resources from passed prop
            currentResources: [
                ...this.instance.resources
            ],

            // @prop    dragOptions
            // @desc    options for vuedraggable instance of resources
            // @        shares group name with the resource list so that resources
            // @        can be passed into section's resources
            dragOptions: {
                handle: ".handle",
                group: "resources"
            },
        }
    },
    methods: {
        // @func    addSection
        // @desc    add a new course activity to the local resources
        // @        and inform parent of data change
        addActivity () {
            this.currentResources.push({
                title: this.$i18n.ACTIVITY_TITLE_NEW,
                type: "CourseActivity",
                uuid: generateUUID()
            })

            this.relayUpdate()
        },

        // @func    relayUpdate
        // @desc    inform parent of data change within section
        relayUpdate () {
            this.$emit("update", { resources: this.currentResources })
        },

        // @func    removeResource
        // @desc    remove selected course resource from local resources
        // @        and inform parent of data change
        removeResource (id) {
            this.currentResources = this.currentResources
                .filter( (resource, index) => (index !== id) )

            this.relayUpdate()
        },

        // @func    updateResource,
        // @desc    on reordering change or any content update of internal resources,
        // @        we need to assign that resource in their new order back to the section
        // @        and inform parent of change
        updateResource ({ instance, $event }) {
            const currentResourceIndex = this.currentResources.findIndex( resource => resource === instance )

            this.currentResources[currentResourceIndex] = $event.resource

            this.relayUpdate()
        }
    }
}
</script>

<template>
<article class="course-section panel panel-primary">
    <header class="course-section-hdr panel-heading flex:h-p:start--s:middle rhy:xStart50">
        <slot name="preheading"></slot>

        <h4 class="panel-title">
            {{ $i18n.SECTION_LABEL }}
        </h4>

        <slot name="postheading"></slot>
    </header>

    <draggable
        class="panel-body pad:xyEq75 rhy:yStart100"
        v-model="currentResources"
        :options ="dragOptions"
        @add="relayUpdate"
        @end="relayUpdate"
    >
        <component
            v-for="(instance, index) in currentResources"
            :instance="instance"
            :is="instance.type"
            :key="instance.uuid || instance.id"
            @update="updateResource({ instance, $event })"
        >
            <template v-slot:preheading>
                <span
                    class="handle glyph"
                    role="button"
                >
                    <img src="/static/orb/images/glyphicons-move.png" />
                </span>
            </template>

            <template v-slot:postheading>
                <icon-control
                    class="pad:xyEq0 iso:xStartAuto"
                    glyph="remove"
                    @click="removeResource(index)"
                >
                    {{ $i18n.RESOURCE_REMOVE }}
                </icon-control>
            </template>
        </component>

        <div
            class="alert alert-warning iso:yEnd0"
            slot="footer"
            v-if="!currentResources.length"
        >
            <p>{{ $i18n.SECTION_EMPTY }}</p>
        </div>
    </draggable>

    <footer class="panel-footer flex:h--p:end--s:middle">
        <action-control
            glyph="plus"
            theme="primary"
            @click="addActivity"
        >
            <span>{{ $i18n.ACTIVITY_ADD }}</span>
        </action-control>
        <slot name="section:footer:controls"></slot>
    </footer>
</article>
</template>
