// @file    store (CourseBuilder)
// @desc    creeates Vuex store for use within CourseBuilder
// @reqs    required Vue, Vuex, and VuexOrm (loaded through vendors/bundle)
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import { Course, User } from "@CourseBuilder/config/models"

Vue.use(Vuex)

const database = new VuexORM.Database()
database.register(Course, {})
database.register(User, {})

export default new Vuex.Store({
    plugins: [VuexORM.install(database, { namespace: "orm" })],
})
