import Vue from 'vue'
import Axios from 'axios'
import CourseEditor from '@/courses/course-editor'

Vue.prototype.$http = Axios

/* eslint-disable no-new */
new Vue({
    el: '#app',
    components: {
        CourseEditor
    }
})
