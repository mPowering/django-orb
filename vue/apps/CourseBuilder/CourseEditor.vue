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
        // @prop    action
        // @desc    determines whether we are in creation or edit mode
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

        // @prop    sections
        // @desc    passed array of course's saved sections and resources
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
            // @prop    availableResources
            // @desc    list of queried resource results from a search
            availableResources: [],

            // @prop    course
            // @desc    locally initialized current course based on passed rops
            course: {
                id: this.id.length > 0 ? this.id : null,
                title: this.title,
                status: this.status,
                sections: this.sections
            },

            // @prop    isTitleEditable
            // @desc    state for showing inputs for update a course title
            isTitleEditable: false,

            // @prop    notification
            // @desc    data object for showing UI alerts and notifications
            notification: {
                active: false,
                status: "info",
                message: ""
            },

            // @prop    q
            // @desc    query string for searching server db for applicable resources
            q: "",

            // @prop    saveAction
            // @desc    initalize base action mode based off passed prop
            saveAction: this.action,
        }
    },
    computed: {
        // @prop    initialCourseView
        // @desc    boolean that determines whether we are in the initial create mode;
        // @        used for showing different UI pieces based on status
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
        // @func    resetNotification
        // @desc    clears out a current notifiction
        resetNotification () { this.notification.active = false },

        // @func    redirectOnCreate
        // @desc    once a course has been created, we need to switch to a new view
        // @        so we don't recreate new courses on subsequent saves
        redirectOnCreate ({ url = this.savepoint }) {
            const logicCheck = (this.initialCourseView && this.course.id)

            if (logicCheck) window.location.replace(url)
        },

        // @func    saveCourse
        // @desc    based on current course status, save or create a course
        // @        assigned return server data to current course
        // @        show a ui notification for success (defaults to 200 template)
        // @        if newly created, redirect to edit form and state
        // @        update the action mode to the update state
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
                } = await api
                        .update({
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
                this.setNotification({status: "500", message: error.message })
            }

            return
        },

        // @func    setNotification
        // @desc    activates the UI notification,
        // @        checks if there is a defined alert template to use based on a status key
        // @        use assigned template or custom messaging
        setNotification ({ status, message = null }) {
            const systemAlert = COURSE_ALERTS[status] || {}

            this.notification = {
                active: true,
                status: systemAlert.status || "info",
                message: systemAlert.message || message
            }
        },

        // @func    setTitleEditState
        // @desc    switch title state from edit to viewable
        setTitleEditState ({ state = !this.isTitleEditable }) {
            this.isTitleEditable = state
        },

        // @func    searchResources
        // @desc    request a queried set of resources from server
        // @        and assign to available resources
        async searchResources () {
            try {
                let { objects: availableResources } = await api
                    .fetch({
                        route: API_ROUTES.RESOURCE_SEARCH,
                        params: {
                            format: "json",
                            q: this.q
                        }
                    })

                this.availableResources = availableResources
            }
            catch (error) { console.log(error) }

            return
        },

        // @func    updateSections
        // @desc    assign current course sections with the passed event's updated sections
        updateSections ({ sections }) {
            this.course.sections = sections
        },

        // @func    updateStatus
        // @desc    publish or draft a current course based on its current-to-desired status
        // @        set status, show a notificaton template, and save the course
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
