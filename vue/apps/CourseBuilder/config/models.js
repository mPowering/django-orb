// @file    models (CourseBuilder)
// @desc    data object models for use within CourseBuilder
// @reqs    required Vuex and VuexOrm (loaded through vendors/bundle)
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import COURSE_STATUS from "@CourseBuilder/config/status.yaml"

import { defaultSectionSchema } from "@CourseBuilder/CourseSection"


// @func    parseTemplateData
// @desc    used to parse json data embedded within a server delivered template
const parseTemplateData = function ({ id }) {
    try {
        return JSON.parse(document.getElementById(id).innerHTML)
    }
    catch (err) {
        return false
    }
}


// @class   User
// @desc    current a simple model to see if user is authenticated,
// @        can be extended over time if needed
export class User extends VuexORM.Model {
    // @desc    object name within Vuex
    static entity = "users"

    // @desc    localized primary key
    static primaryKey = "id"

    // @desc    normalized data for the UI
    static fields () {
        return {
            id: this.increment(),
            isAuthenticated: this.boolean(false)
        }
    }

    // @domain  Store model interface: bulk
    // ++++++++++++++++++++++++++++++++++++++

    // @func    stageFromTemplate
    // @desc    look for <script #userData> and load it as JSON into our model
    static async stageFromTemplate () {
        try {
            let data = parseTemplateData({ id: "userData" })

            if (data) await User.insertOrUpdate({ data })
            else {
                data = await new User()
                await User.insertOrUpdate({ data })
            }
        }
        catch (err) {}

        return
    }
}


// @class   Course
// @desc    data model for current course structures
export class Course extends VuexORM.Model {
    // @desc    object name within Vuex
    static entity = "courses"

    // @desc    localized primary key
    static primaryKey = "id"

    // @desc    normalized data for the UI
    static fields () {
        return {
            exportRoutes: this.attr({}),
            id: this.attr(),
            sections: this.attr([defaultSectionSchema]),
            status: this.string(COURSE_STATUS.UPDATE),
            title: this.string("New Course"),
            url: this.string()
        }
    }

    static state = {
        $registered: false, // recalled from or saved to the server
        $synced: false, // UI has changed value props and differs from server
    }

    // @domain  Store model interface: bulk
    // ++++++++++++++++++++++++++++++++++++++

    // @func    stageFromTemplate
    // @desc    look for <script #courseData> and load it as JSON into our model
    // @        - this is used when reloading on a course detail/form page as the JSON exposes that current data model
    // @        look for <script #courseListData> and load it as JSON into our model
    // @        - this is used when reloading on the course list page as the JSON exposes all curent course data models
    static async stageFromTemplate () {
        if (Course.state.$registered) return

        try {
            let courseSchema = parseTemplateData({ id: "courseData" })
            let courses = parseTemplateData({ id: "courseListData" })

            if (courseSchema) await Course.insertOrUpdate({ data: courseSchema })
            if (courses) await Course.insertOrUpdate({ data: courses })

            Course.state.$registered = true
        }
        catch (err) {}

        return
    }

}
