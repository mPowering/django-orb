import Vue from "vue"
// import Vuex from "vuex"
// Vue.use(Vuex)
// import { Model } from "@vuex-orm/core"
// import VueRouter from 'vue-router'
// Vue.use(VueRouter)
// @note    lets increase performance for production
Vue.config.performance = process.env.NODE_ENV !== "production"

// @plugin      i18n
// @desc        exposes $i18n, data object mapping internationalizations for app
import i18nDefaults from "@CourseBuilder/config/translations"
import i18n from "@services/i18n"
Vue.use(i18n, {
    defaultTranslations: i18nDefaults
})

import "@apps/course_builder.css"
import CourseEditor from "@CourseBuilder/CourseEditor"

import ActionControl from "@controls/ActionControl"
Vue.component("ActionControl", ActionControl)

import IconControl from "@controls/IconControl"
Vue.component("IconControl", IconControl)

/* eslint-disable no-new */
new Vue({
    name: "Orb",
    el: '#app',
    components: {
        CourseEditor
    }
})
