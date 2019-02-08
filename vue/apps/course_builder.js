import "@apps/course_builder.css"

// import Vue from "vue"

// @note    lets increase performance for production
Vue.config.performance = process.env.NODE_ENV !== "production"

// @plugin      i18n
// @desc        exposes $i18n, data object mapping internationalizations for app
import i18n from "@services/i18n"
Vue.use(i18n, {
    translations: window.i18n || {}
})

import store from "@CourseBuilder/config/store"
import router from "@CourseBuilder/config/routes"

import { Course, User } from "@CourseBuilder/config/models"

/* eslint-disable no-new */
new Vue({
    name: "Orb",
    router,
    template: "<router-view></router-view>",

    // @lifecycle   created
    // @desc        on initial loading of the page,
    // @            load in template data into the store
    async created () {
        try {
            await Course.stageFromTemplate()
            await User.stageFromTemplate()
        }
        catch (error) {
            console.log(error)
        }
        return
    },
}).$mount("#app")
