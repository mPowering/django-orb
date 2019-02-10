<script>
import COURSE_STATUS from "@CourseBuilder/config/status"
import COURSE_ALERTS from "@CourseBuilder/config/alerts"

import { api } from "@services/api"

import { Course, User } from "@CourseBuilder/config/models"

import Draggable from "vuedraggable"

import { defaultSectionSchema } from "@CourseBuilder/CourseSection"
import DismissableNotification from "@notifications/DismissableNotification"
import PrimaryBreadcrumbs from "@navigation/PrimaryBreadcrumbs"
import ResourceList from "@CourseBuilder/ResourceList"
import SectionRiver from "@CourseBuilder/SectionRiver"


export default {
    name: "CourseEditor",
    components: {
        DismissableNotification,
        Draggable,
        PrimaryBreadcrumbs,
        ResourceList,
        SectionRiver,
    },
    props: {
        editable: {
            type: Boolean,
            default: false
        },

        // @prop    exportRoutes
        // @desc    object for Moodle and Oppia export routes
        exportRoutes: {
            type: Object,
            default: () => ({})
        },

        // @prop    id
        // @desc    server-based/synced course id
        id: {
            type: [Boolean, String, Number],
            default: false
        },

        // @prop    sections
        // @desc    passed array of course's saved sections and resources
        sections: {
            type: Array,
            default: () => ([defaultSectionSchema])
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
            type: [Boolean, String],
            default: false
        },
    },
    data () {
        return {
            // @prop    course
            // @desc    locally initialized current course based on passed rops
            course: new Course({
                editable: this.editable,
                exportRoutes: this.exportRoutes || {},
                id: this.id.length ? this.id : "",
                title: this.title || this.$i18n.COURSE_TITLE_NEW,
                status: this.status || COURSE_STATUS.INACTIVE,
                sections: this.sections || [defaultSectionSchema],
            }),

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

            // @prop    saveAction
            // @desc    initalize base action mode based off passed prop
            saveAction: this.$route.meta.action,
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

        // @prop    routes
        // @desc    define local api routes based on course id
        routes () {
            return {
                [COURSE_STATUS.CREATE]: `${ this.$router.resolve({ name: "createCourse" }).href }/`,
                [COURSE_STATUS.UPDATE]: `${ this.$router.resolve({ name: "editCourse", params: { id: this.course.id } }).href }/`,
            }
        },
        // @prop    user
        // @desc    get the current user from the Vuex Store
        user () {
            return User.query().first()
        }
    },
    watch: {
        // @prop    $route
        // @desc    run on change/instantiation for boilerplate work
        $route: {
            immediate: true,
            handler () {
                // @info    this is a driver for when we have a hard-reload on the page,
                // @        as VueRouter passes everything else to the component props
                // @        if we're on a new course form, we don't need to go to the store
                // @        if on a reloaded course detail form, get the first store entry (comes from template)
                // @        this.id is automatically provided by VueRouter
                if (this.$route.meta.action == COURSE_STATUS.CREATE) {
                    this.course.editable = true
                } else {
                    this.course = Course.find(this.id)
                }
                return
            }
        }
    },
    methods: {
        // @func    getExportRoutes
        // @desc    after saving a new course, we don't have the
        // @        course's export routes as those are provided by the template, instead:
        // @        - fetch the course's detail page via Ajax
        // @        - parse the html
        // @        - get the <script #courseData> json and load it into a local variable
        // @        - update the exportRoutes for the current course and save to the Vuex Store
        async getExportRoutes ({ id } = { id: this.course.id }) {
            try {
                const parser = new DOMParser()
                let html = await api.fetch({ route: this.routes[COURSE_STATUS.UPDATE] })
                const { exportRoutes } = JSON.parse(
                    parser
                        .parseFromString(html, "text/html")
                        .querySelector("#courseData")
                        .innerHTML
                )
                this.course.exportRoutes = exportRoutes
                await this.course.$save()
            }
            catch (err) {}
            return
        },

        // @func    redirectOnCreate
        // @desc    once a course has been created, we need to switch to a new view
        // @        so we don't recreate new courses on subsequent saves
        async redirectOnCreate ({ id } = { id: this.course.id }) {
            const logicCheck = (this.initialCourseView && id)

            try {
                if (logicCheck) {
                    await this.getExportRoutes({ id })

                    let params = {
                        ...this.course
                    }

                    delete params.$id

                    this.$router.replace({
                        name: "editCourse",
                        params
                    })
                }
            }
            catch (err) {}
            return
        },

        // @func    resetNotification
        // @desc    clears out a current notifiction
        resetNotification () { this.notification.active = false },

        // @func    saveCourse
        // @desc    based on current course status, save or create a course
        // @        assigned return server data to current course
        // @        show a ui notification for success (defaults to 200 template)
        // @        if newly created, redirect to edit form and state
        // @        update the action mode to the update state
        async saveCourse ({ status = "200" }) {
            const route = this.routes[this.saveAction]
            const data = this.course

            try {
                const {
                    course_id,
                    course_status,
                    message,
                    url
                } = await api
                        .update({ route, data })

                this.course.id = course_id
                this.course.status = course_status

                await this.course.$save()
                this.setNotification({ status, message })
                await this.redirectOnCreate()
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

        // @func    updateSections
        // @desc    assign current course sections with the passed event's updated sections
        updateSections ({ sections }) {
            this.course.sections = sections
        },

        // @func    updateStatus
        // @desc    publish or draft a current course based on its current-to-desired status
        // @        set status, show a notificaton template, and save the course
        async updateStatus () {
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

            try {
                this.course.status = updateStatus[status].courseStatus
                await this.saveCourse({ status: updateStatus[status].msgStatus })
            }
            catch (error) {}

        }
    }
}
</script>

<template>
<article class="course-editor flex:h--p:start grid:h--cols:iAuto--gaps:xyEq100">
    <div>
        <header class="course-editor-hdr flex:h--p:start--s:middle pad:yEq100">
            <h2 class="course-editor-hed flex:hAuto--p:start--s:middle rhy:xStart50 iso:yEq0"
                v-if="!isTitleEditable"
                @click="setTitleEditState"
            >
                <span>{{ course.title }}</span>

                <action-control
                    class="course-editor-hed-edit btn-xs pad:xyEq25"
                    glyph="edit"
                    theme="primary"
                    v-if="course.editable"
                >
                    <span class="sr-only">{{ $i18n.COURSE_TITLE_EDIT }}</span>
                </action-control>
            </h2>

            <div
                class="flex:hAuto--p:start--s:start"
                v-else
            >
                <input
                    class="form-control module:static"
                    v-model="course.title"
                >

                <div class="input-group-btn module:static">
                    <action-control
                        class="course-editor-hed-save"
                        @click="setTitleEditState"
                    >
                        {{ $i18n.COURSE_TITLE_SAVE }}
                    </action-control>
                </div>
            </div>
        </header>

        <div
            class="lead panel"
            v-html="$i18n.EDITOR_CONTENT"
            v-if="initialCourseView && $i18n.EDITOR_CONTENT"
        ></div>

        <section class="editor-river">
            <dismissable-notification
                class="iso:yEnd100"
                v-bind="notification"
                @dismissed="resetNotification"
            ></dismissable-notification>

            <section-river
                :can-edit="course.editable"
                :sections="course.sections"
                @update="updateSections"
            ></section-river>
        </section>
    </div>

    <aside class="editor-sidebar pad:yEq100">
        <div class="module:sticky">
            <primary-breadcrumbs class="iso:yEnd100"></primary-breadcrumbs>

            <template v-if="course.editable">
                <div class="btn-group flex:h--p:start--s:middle pad:yEq100 iso:yEnd100 edge:yEq--def:tint">
                    <action-control
                        class="btn-sm module:balance"
                        v-bind="saveControlMeta"
                        @click="saveCourse"
                    >
                        <span>{{ saveControlMeta.label }}</span>
                    </action-control>

                    <action-control
                        class="btn-sm module:balance"
                        v-bind="statusControlMeta"
                        v-if="course.id"
                        @click="updateStatus"
                    >
                        <span>{{ statusControlMeta.label }}</span>
                    </action-control>
                </div>
            </template>

            <div
                class="pad:yEnd100 iso:yEnd100 rhy:yStart50 edge:yEnd--def:tint"
                v-if="course.id"
            >
                <div class="btn-group flex:h--p:start--s:middle">
                    <action-link
                        class="btn-sm module:balance"
                        v-if="course.exportRoutes.moodleExport"
                        :href="course.exportRoutes.moodleExport"
                    >
                        {{ $i18n.EXPORT_MOODLE }}
                    </action-link>

                    <action-link
                        class="btn-sm module:balance"
                        v-if="course.exportRoutes.oppiaExport"
                        :href="course.exportRoutes.oppiaExport"
                    >
                        {{ $i18n.EXPORT_OPPIA }}
                    </action-link>
                </div>

                <action-link
                    class="btn-sm module:balance"
                    theme="primary"
                    v-if="course.exportRoutes.oppiaPublish"
                    :href="course.exportRoutes.oppiaPublish"
                >
                    {{ $i18n.EXPORT_OPPIA_PUBLISH }}
                </action-link>
            </div>

            <resource-list
                class="list-group"
                v-if="course.editable"
            ></resource-list>
        </div>
    </aside>
</article>
</template>

<style>
.course-editor {
    --gridCols: minmax(min-content, 70%) minmax(auto, 1fr)
}

.editor-river {
    position: sticky;
    top: 86px;
}

.editor-river .alert {
    padding: 4px 35px 4px 12px;
}

.editor-sidebar > [class*="module:sticky"] {
    position: sticky;
    top: 86px;
}
</style>
