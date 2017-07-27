<template src="./course-editor.html"></template>
<style module src="../module.css"></style>

<script>
import CourseSection from '@/courses/course-section'
import CourseResource from '@/courses/course-resource'
import draggable from 'vuedraggable'

const defaults = {
    sections: [{resources: []}],
    endpoints: {
        api: '/api/v1/',
        resource_search: `/api/v1/resource/search/`,
        create: '.',
        update: '/courses/:id/'
    }
}

export default {
    name: 'course-editor',
    components: {
        draggable,
        CourseSection,
        CourseResource
    },
    props: {
        id: String,
        title: {
            type: String,
            default: 'New Course'
        },
        sections: {
            type: Array,
            default: () => (defaults.sections)
        },
        labels: {
            type: Object,
            default: () => ({
                edit_title: 'Edit Course Title',
                save_title: 'Save Course Title',
                add_section: 'Add Course Section',
                remove_section: 'Remove Course Section',
                add_activity: 'Add Text Activity',
                create: 'Create Course',
                save: 'Save Course',
                search: 'Search',
                new_course_title: 'New Course'
            })
        },
        action: {
            type: String,
            default: 'update'
        }
    },
    data () {
        return {
            course_id: this.id || false,
            course_title: this.title,
            course_sections: this.sections,
            save_action: this.action,
            edit_head: false,
            q: '',
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

            return this.$http.post(this.savepoint, course)
                .then(
                    (response) => {
                        this.course_id = response.data.course_id
                        this.save_action = 'update'
                    }
                )
                .catch(
                    (error) => console.error(error)
                )
        },
        searchResources () {
            this.$http.get(
                defaults.endpoints.resource_search,
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
    computed: {
        savepoint () {
            let savepoint = (this.save_action === 'update') ? defaults.endpoints.update : defaults.endpoints.create
            return savepoint.replace(':id', this.course_id)
        },
        save_label () {
            return (this.save_action === 'update') ? this.labels.save : this.labels.create
        }
    },
    created () {
        if (this.labels.new_course_title && !this.title) {
            this.course_title = this.labels.new_course_title
        }
        if (this.sections.length === 0) {
            this.course_sections = defaults.sections
        }
    }
}
</script>
