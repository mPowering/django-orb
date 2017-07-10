<template src="./course-editor.html"></template>
<style module src="../module.css"></style>

<script>
import CourseSection from '@/courses/course-section'
import CourseResource from '@/courses/course-resource'
import draggable from 'vuedraggable'

export default {
    name: 'course-editor',
    components: {
        draggable,
        CourseSection,
        CourseResource
    },
    props: {
        title: {
            type: String,
            default: 'New Course'
        },
        sections: {
            type: Array,
            default: () => ([])
        },
        labels: {
            type: Object,
            default: () => ({
                edit_title: 'Edit Course Title',
                save_title: 'Save Course Title',
                add_section: 'Add Course Section',
                remove_section: 'Remove Course Section',
                add_activity: 'Add Text Activity',
                save: 'Save Course',
                search: 'Search',
                new_course_title: 'New Course'
            })
        }
    },
    data () {
        return {
            course_title: this.title,
            course_sections: this.sections,
            edit_head: false,
            q: '',
            resource_api: '/api/v1/',
            available_resources: []
        }
    },
    methods: {
        editTitle () { this.edit_head = true },
        saveTitle () { this.edit_head = false },
        addSection () {
            this.course_sections.push({
                resources: []
            })
        },
        removeSection (id) {
            this.course_sections = this.course_sections.filter(
                (section, index) => {
                    return index !== id
                }
            )
        },
        saveCourse () {
            let course = {
                title: this.course_title,
                sections: this.course_sections,
            }

            this.$http.post('.', course)
                .then(
                    (response) => {}
                )
                .catch(
                    (error) => console.error(error)
                )
        },
        searchResources () {
            this.$http.get(
                `${this.resource_api}resource/search/`,
                {
                    params: {
                        format: 'json',
                        q: this.q
                    }
                }
            )
                .then(
                    (response) => {
                        this.available_resources = response.data.objects
                    }
                )
                .catch(
                    (error) => console.error(error)
                )
        }
    },
    beforeMount () {
        if (this.labels.new_course_title && !this.title) {
            this.course_title = this.labels.new_course_title
        }
    }
}
</script>
