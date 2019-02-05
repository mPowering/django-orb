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
        instance: {
            type: Object,
            default: () => ({})
        }
    },
    data () {
        return {
            dragOptions: {
                handle: ".handle",
                group: "resources"
            },
            currentResources: [
                ...this.instance.resources
            ]
        }
    },
    methods: {
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

        removeResource (id) {
            this.currentResources = this.currentResources.filter(
                (resource, index) => (index !== id)
            )
            this.relayUpdate()
        },

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
    <header class="course-section-hdr panel-heading flex:h-p:start--s:middle rhy:xStart25">
        <slot name="section:preheading"></slot>

        <h4 class="panel-title">
            {{ $i18n.SECTION_LABEL }}
        </h4>

        <slot name="section:postheading"></slot>
    </header>

    <draggable
        class="panel-body pad:yEnd0"
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
            <template slot="entry:preheading">
                <span
                    class="handle glyph pad:xEq25"
                    role="button"
                >
                    <img src="/static/orb/images/glyphicons-move.png" />
                </span>
            </template>

            <template slot="entry:postheading">
                <icon-control
                    class="iso:xStartAuto"
                    glyph="remove"
                    @click="removeResource(index)"
                >
                    {{ $i18n.RESOURCE_REMOVE }}
                </icon-control>
            </template>
        </component>

        <div
            class="alert alert-warning"
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

<style>
.course-section-hdr .handle {
    cursor: grab
}
.course-section-hdr .handle > img {
    height: 16px;
    margin-top: -5px;
    width: 16px;
}
</style>
