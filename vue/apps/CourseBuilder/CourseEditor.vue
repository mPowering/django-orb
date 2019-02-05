<script>
import COURSE_STATUS from "@CourseBuilder/config/status"
import COURSE_ALERTS from "@CourseBuilder/config/alerts"

import { api } from "@services/api"
import API_ROUTES from "@CourseBuilder/config/apiRoutes"

import Draggable from "vuedraggable"

import DismissableNotification from "@notifications/DismissableNotification"
import ResourceList from "@CourseBuilder/ResourceList"
import SearchField from "@fields/SearchField"
import SectionRiver from "@CourseBuilder/SectionRiver"

const defaultSectionSchema = { resources: [] }

export default {
    name: "CourseEditor",
    components: {
        DismissableNotification,
        Draggable,
        ResourceList,
        SearchField,
        SectionRiver,
    },
    props: {
        action: {
            type: String,
            default: COURSE_STATUS.UPDATE
        },

        // @prop    id
        // @desc    server-based/synced course id
        id: {
            type: [Boolean, String],
            default: false
        },

        sections: {
            type: Array,
            default: () => ([[defaultSectionSchema]])
        },

        // @prop    status
        // @desc    the current publish state of the course
        status: {
            type: String,
            default: COURSE_STATUS.INACTIVE
        },

        // @prop    title
        // @desc    the title for the current course
        title: {
            type: String,
            default: () => this.$i18n.COURSE_TITLE_NEW
        },
    },
    data () {
        return {
            availableResources: [],
            course: {
                id: this.id.length > 0 ? this.id : null,
                title: this.title,
                status: this.status,
                sections: this.sections
            },
            isTitleEditable: false,
            notification: {
                active: false,
                status: "info",
                message: ""
            },
            q: "",
            saveAction: this.action,
        }
    },
    computed: {
        initialCourseView () {
            return (this.saveAction === COURSE_STATUS.CREATE)
        },

        // @prop    saveControlMeta
        // @desc    determines properties for save control based on course action status
        saveControlMeta () {
            return {
                disabled: this.course.sections.length < 1,
                glyph: "ok-circle",
                label: (this.saveAction === COURSE_STATUS.UPDATE)
                    ? this.$i18n.COURSE_SAVE
                    : this.$i18n.COURSE_CREATE,
                theme: "success",
            }
        },

        // @prop    statusControlMeta
        // @desc    determines properties for publishing control based on course draft status
        statusControlMeta () {
            return (this.course.status === COURSE_STATUS.INACTIVE)
                ? {
                    glyph: "cloud-download",
                    label: this.$i18n.COURSE_SET_PUBLISH,
                    theme: "default"
                }
                : {
                    glyph: "cloud-upload",
                    label: this.$i18n.COURSE_SET_DRAFT,
                    theme: "primary",
                }
        },
    },
    methods: {
        resetNotification () { this.notification.active = false },

        redirectOnCreate ({ url = this.savepoint }) {
            const logicCheck = (this.initialCourseView && this.course.id)
            if (logicCheck) window.location.replace(url)
        },

        async saveCourse ({ status = "200" }) {
            try {
                let route = (this.saveAction === COURSE_STATUS.CREATE)
                    ? API_ROUTES.CREATE
                    : API_ROUTES.UPDATE.replace(":id", this.course.id)

                const {
                    course_id,
                    course_status,
                    message,
                    url
                } = await api.update({
                        route,
                        data: this.course
                    })

                this.course.id = course_id
                this.course.status = course_status
                this.setNotification({ status, message })
                this.redirectOnCreate({ url })
                this.saveAction = COURSE_STATUS.UPDATE
            }
            catch (error) {
                this.setNotification({status: "500", message })
            }

            return
        },

        setNotification ({ status, message = null }) {
            const systemAlert = COURSE_ALERTS[status] || {}

            this.notification = {
                active: true,
                status: systemAlert.status || "info",
                message: systemAlert.message || message
            }
        },

        setTitleEditState ({ state = !this.isTitleEditable }) {
            this.isTitleEditable = state
        },

        // @func    searchResources
        // @desc    request a queried set of resources from server
        // @        and assign to available resources
        async searchResources () {
            try {
                let { objects: availableResources } = await api.fetch(
                    {
                        route: API_ROUTES.RESOURCE_SEARCH,
                        params: {
                            format: "json",
                            q: this.q
                        }
                    }
                )

                this.availableResources = availableResources
            }
            catch (error) { console.log(error) }

            return
        },
        updateSections ({ sections }) {
            this.course.sections = sections
        },
        updateStatus () {
            const { status } = this.course
            const updateStatus = {
                [COURSE_STATUS.ACTIVE]: {
                    courseStatus: COURSE_STATUS.INACTIVE,
                    msgStatus: "200-draft"
                },
                [COURSE_STATUS.INACTIVE]: {
                    courseStatus: COURSE_STATUS.ACTIVE,
                    msgStatus: "200-publish"
                }
            }

            this.course.status = updateStatus[status].courseStatus
            this.saveCourse({ status: updateStatus[status].msgStatus })

        }
    }
}
</script>

<template>
<article class="course-editor">
    <header class="course-editor-hdr iso:yEnd50">
        <h3 class="course-editor-hed col-sm-6 flex:h--p:start--s:middle rhy:xStart50"
            v-if="!isTitleEditable"
            @click="setTitleEditState"
        >
            <span>{{ course.title }}</span>

            <action-control
                class="course-editor-hed-edit btn-xs pad:xyEq25"
                glyph="edit"
                theme="primary"
            >
                <span class="sr-only">{{ $i18n.COURSE_TITLE_EDIT }}</span>
            </action-control>
        </h3>

        <div
            class="input-group col-sm-6 pad:xEq50"
            v-else
        >
            <input
                class="form-control"
                v-model="course.title"
            >

            <div class="input-group-btn">
                <action-control
                    class="course-editor-hed-save"
                    @click="setTitleEditState"
                >
                    {{ $i18n.COURSE_TITLE_SAVE }}
                </action-control>
            </div>
        </div>


    </header>

    <div class="row">
        <section class="course-sections col-sm-9">
            <dismissable-notification
                v-bind="notification"
                @dismissed="resetNotification"
            ></dismissable-notification>

            <section-river
                :sections="course.sections"
                @update="updateSections"
            ></section-river>

            <div class="btn-group">
                <action-control
                    class="course-save-ctrl"
                    v-bind="saveControlMeta"
                    @click="saveCourse"
                >
                    <span>{{ saveControlMeta.label }}</span>
                </action-control>

                <action-control
                    class="course-publish-ctrl"
                    v-bind="statusControlMeta"
                    v-if="course.id"
                    @click="updateStatus"
                >
                    <span>{{ statusControlMeta.label }}</span>
                </action-control>
            </div>
        </section>

        <aside class="resource-search col-sm-3">
            <search-field
                v-model="q"
                @submit="searchResources"
            >
                {{ $i18n.RESOURCE_LABEL_SEARCH }}
            </search-field>

            <resource-list
                class="list-group"
                :resources="availableResources"
            ></resource-list>
        </aside>
    </div>
</article>
</template>
