<script>
import COURSE_STATUS from "@CourseBuilder/config/status"

import { Course, User } from "@CourseBuilder/config/models"

export default {
    name: "CourseList",
    computed: {
        // @prop    courses
        // @desc    course data retrieved from Vuex store
        courses () {
            return Course.query().orderBy("title").all()
        },

        // @prop    user
        // @desc    user data retrieved from Vuex store
        // @        primaryly used for hiding and show template elements based on user authentication
        user () {
            return User.query().first() || {}
        },

        // @prop    processedCourses
        // @desc    map course data with:
        // @        - the local theme style for their badge
        // @        - remove $id (VuexOrm key) from data as it breaks VueRouter
        processedCourses () {
            return this.courses.map(
                course => {
                    let instance = {
                        ...course,
                        labelTheme: this.isDraft(course) ? "warning" : "success"
                    }
                    delete instance.$id
                    return instance
                }
            )
        },

        // @prop    newCourseRouteParams
        // @desc    router data object for navigating to new course form
        newCourseRouteParams () {
            return {
                name: "createCourse",
                params: {
                    editable: true,
                    action: COURSE_STATUS.CREATE
                }
            }
        },
    },
    methods: {
        // @func    isDraft
        // @desc    determine if a passed course is in draft status
        isDraft ({ status }) {
            return status === COURSE_STATUS.INACTIVE
        }
    },
}
</script>

<template>
<section>
    <header class="flex:h--p:start--s:middle pad:yEq100">
        <h2 class="flex:hAuto--p:start--s:middle rhy:xStart50 iso:yEq0">
            {{ $i18n.COURSES_LABEL }}
        </h2>

        <template v-if="user.isAuthenticated">
            <router-control
                class="iso:xStartAuto"
                glyph="edit"
                :link="newCourseRouteParams"
            >
                <span>{{ $i18n.COURSE_ADD }}</span>
            </router-control>
        </template>
    </header>

    <div
        class="lead panel"
        v-html="$i18n.COURSES_CONTENT"
        v-if="$i18n.COURSES_CONTENT"
    ></div>

    <template v-if="processedCourses.length">
        <div
            class="module:static flex:h--p:start--s:middle pad:yEq100 rhy:xStart50"
            :class="{ 'edge:yStart--def:tint': index > 0 }"
            v-for="(course, index) in processedCourses"
            :key="course.id"
        >

            <h4>
                <router-link
                    class="flex:hAuto--p:start--s:base"
                    :to="{ name: 'editCourse', params: { ...course } }"
                >
                    {{ course.title }}
                </router-link>
            </h4>

            <div
                class="label pad:xyEq25 iso:xStartAuto iso:xEnd50"
                :class="`label-${ course.labelTheme }`"
            >
                {{ course.status }}
            </div>

            <div
                class="btn-group"
                v-if="user.isAuthenticated"
            >
                <action-link
                    class="btn-sm"
                    v-if="course.exportRoutes.moodleExport"
                    :href="course.exportRoutes.moodleExport"
                >
                    {{ $i18n.EXPORT_MOODLE }}
                </action-link>

                <action-link
                    class="btn-sm"
                    v-if="course.exportRoutes.oppiaExport"
                    :href="course.exportRoutes.oppiaExport"
                >
                    {{ $i18n.EXPORT_OPPIA }}
                </action-link>

                <action-link
                    class="btn-sm"
                    theme="primary"
                    v-if="course.exportRoutes.oppiaPublish"
                    :href="course.exportRoutes.oppiaPublish"
                >
                    {{ $i18n.EXPORT_OPPIA_PUBLISH }}
                </action-link>
            </div>
        </div>
    </template>

    <template v-if="!processedCourses.length && user.isAuthenticated">
        <div
            class="alert alert-warning flex:h--p:start--s:middle rhy:xStart50"
        >
            <p>{{ $i18n.COURSES_EMPTY }}</p>

            <router-control
                class="iso:xStartAuto"
                glyph="edit"
                theme="warning"
                :link="{ name: 'createCourse' }"
            >
                <span>{{ $i18n.COURSE_ADD }}</span>
            </router-control>
        </div>
    </template>

    <div
        class="alert alert-warning flex:h--p:start--s:middle rhy:xStart50"
        v-if="!user.isAuthenticated"
    >
            <p v-html="$i18n.LOGIN_WARNING"></p>
    </div>
</section>
</template>
