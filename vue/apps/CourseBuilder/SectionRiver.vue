<script>
import { generateUUID } from "@utils/uuid"

import Draggable from "vuedraggable"

import CourseSection, { defaultSectionSchema } from "@CourseBuilder/CourseSection"


export default {
    name: "SectionRiver",
    components: {
        Draggable,
        CourseSection
    },
    props: {
        // @prop    sections
        // @desc    current Course's assigned sections
        sections: {
            type: Array,
            default: () => ([])
        }
    },
    data () {
        return {
            // @prop    currentSections
            // @desc    initiate local sections with passed prop
            currentSections: [],

            // @prop    dragOptions
            // @desc    options for vuedraggable instance
            dragOptions: {
                handle: ".handle"
            }
        }
    },
    watch: {
        // @prop    sections
        // @desc    match local currentSections to prop sections
        sections: {
            immediate: true,
            handler () {
                this.currentSections = this.sections.map(
                    section => {
                        // @info    earlier sections don't have a UUID, so we want to ensure
                        // @        we generate one for use with reordering
                        if (!section.uuid) section.uuid = generateUUID()
                        return section
                    }
                )
            }
        }
    },
    methods: {
        // @func    addSection
        // @desc    add a new course section to the local sections
        // @        and inform parent of data change
        addSection () {
            this.currentSections.push({
                // @info    add a uuid so that we can better reorder
                uuid: generateUUID(),
                // @info    this comes after to overwrite uuid if included
                ...defaultSectionSchema
            })

            this.relayUpdate()
        },

        // @func    relayUpdate
        // @desc    inform parent of data change within list
        relayUpdate () {
            this.$emit("update", { sections: this.currentSections })
        },

        // @func    removeSection
        // @desc    remove selected course section from local sections
        // @        and inform parent of data change
        removeSection (id) {
            this.currentSections = this.currentSections
                .filter( (section, index) => (index !== id) )

            this.relayUpdate()
        },

        // @func    updateSection,
        // @desc    on reordering change of sections,
        // @        we need to assign those resources in their new order back to the section
        // @        and inform parent of change
        updateSection ({ instance, $event }) {
            // @info    get the current section by its current index
            const currentSectionIndex = this.currentSections.findIndex( section => section === instance )

            this.currentSections[currentSectionIndex].resources = $event.resources

            this.relayUpdate()
        }
    }
}
</script>

<template>
<draggable
    v-model="currentSections"
    :options="dragOptions"
    @end="relayUpdate"
>
    <course-section
        v-for="(instance, index) in currentSections"
        :instance="instance"
        :key="instance.uuid"
        @update="updateSection({ instance, $event })"
    >
        <template slot="section:preheading">
            <span
                class="handle glyph pad:xEq25"
                role="button"
            >
                <img src="/static/orb/images/glyphicons-move.png" />
            </span>
        </template>

        <template slot="section:postheading">
            <icon-control
                class="iso:xStartAuto"
                glyph="remove"
                @click="removeSection(index)"
            >
                {{ $i18n.SECTION_REMOVE }}
            </icon-control>
        </template>
    </course-section>

    <template slot="footer">
        <div
            class="course-sections-add panel panel-default"
        >
            <button
                class="fake-btn flex:h--p:start--s:base rhy:xStart25"
                type="button"
                @click="addSection"
            >
                <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
                <span>{{ $i18n.SECTION_ADD }}</span>
            </button>
        </div>
    </template>
</draggable>
</template>
