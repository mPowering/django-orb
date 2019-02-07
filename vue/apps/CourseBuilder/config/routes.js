// import Vue from "vue"
// import VueRouter from 'vue-router'
Vue.use(VueRouter)

import COURSE_STATUS from "@CourseBuilder/config/status"

import CourseEditor from "@CourseBuilder/CourseEditor"
import CourseList from "@CourseBuilder/CourseList"

// // @component   universal action control/button
import ActionControl from "@controls/ActionControl"
Vue.component("ActionControl", ActionControl)

// @component   universal action btton-like link
import ActionLink from "@controls/ActionLink"
Vue.component("ActionLink", ActionLink)

// @component   universal icon-only control
import IconControl from "@controls/IconControl"
Vue.component("IconControl", IconControl)

// @component   universal router-link control/button
import RouterControl from "@controls/RouterControl"
Vue.component("RouterControl", RouterControl)


const routes = [
    {
        name: "courseList",
        path: "/",
        component: CourseList,
    },
    {
        name: "createCourse",
        path: "/new",
        component: CourseEditor,
        props: true,
        meta: {
            // @info    this lets s know the primary action is to create a course
            action: COURSE_STATUS.CREATE
        }
    },
    {
        name: "editCourse",
        path: "/:id",
        component: CourseEditor,
        props: true,
        meta: {
            // @info    this lets s know the primary action is to update a course
            action: COURSE_STATUS.UPDATE
        }
    }
]

export default new VueRouter({
    mode: "history",
    base: "/courses",
    routes,
})
