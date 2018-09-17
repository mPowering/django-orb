<template src="./course-editor.html"></template>
<style module src="../module.css"></style>
<style>
.fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}
</style>

<script>
import draggable from 'vuedraggable'
import CourseSection from '@cmp/course-section/course-section'
import CourseResource from '@cmp/course-resource/course-resource'
import CourseNotification from '@cmp/notifications/dismissable'
import PublishControl from '@cmp/course-publish-control/course-publish-control'

const defaults = {
    sections: [[{resources: []}]],
    endpoints: {
        api: '/api/v1/',
        resource_search: `/api/v1/resource/search/`,
        create: '.',
        update: '/courses/:id/'
    },
    status: {
        active: 'published',
        inactive: 'draft'
    },
    alerts: {
        '200': {
            status: 'success',
            message: 'The course was saved successfully.'
        },
        '200-publish': {
            status: 'success',
            message: 'The course is now published.'
        },
        '200-draft': {
            status: 'success',
            message: 'The course is now in draft status.'
        },
        '500': {
            status: 'danger',
            message: `
                Your course was not saved at this time due to an error.
            `
        }
    }
}

export default {
    name: 'course-editor',
    components: {
        draggable,
        CourseSection,
        CourseResource,
        CourseNotification,
        PublishControl
    },
    props: {
        id: String,
        title: {
            type: String,
            default: 'New Course'
        },
        status: {
            type: String,
            default: 'draft'
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
            course_status: this.status,
            course_sections: this.sections,
            save_action: this.action,
            edit_head: false,
            q: '',
            available_resources: [],
            alertUser: false,
            alertStatus: 'info',
            alertMessage: ''
        }
    },
    methods: {
        editTitle () { this.edit_head = true },
        saveTitle () { this.edit_head = false },
        resetAlert () { this.alertUser = false },
        showAlert (status, givenMessage = null) {
            const systemAlert = defaults.alerts[status]
            if (systemAlert) {
                this.alertStatus = systemAlert.status
                this.alertMessage = givenMessage || systemAlert.message
                this.alertUser = true
            }
        },
        mapStatus (givenStatus) { return (defaults.status[givenStatus]) },
        updateStatus () {
            this.course_status = (this.mappedStatus === 'active')
                ? this.mapStatus('inactive')
                : this.mapStatus('active')

            this.saveCourse()
        },
        addSection () { this.course_sections.push({ resources: [] }) },
        removeSection (id) {
            this.course_sections = this.course_sections.filter(
                (section, index) => (index !== id)
            )
        },
        saveCourse () {
            let course = {
                title: this.course_title,
                status: this.course_status,
                sections: this.course_sections,
            }

            return this.$http.post(this.savepoint, course)
                .then(
                    (response) => {
                        this.course_id = response.data.course_id
                        this.redirectOnCreate(response.data.url)
                        this.showAlert('200', response.data.message)
                        this.save_action = 'update'
                    }
                )
                .catch(
                    (error) => {
                        this.showAlert('500')
                        throw error
                    }
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
                        const availableResources = response.data.objects

                        let testing = availableResources.map(
                            ({ title, files }) => {
                                files.forEach(file => { file.title = `${file.title} (${file.file_extension}) - ${title}` })
                                return files
                            }
                        )
                        const resourcesFiles = testing.reduce((acc, val) => acc.concat(val), [])
                        this.available_resources = resourcesFiles.filter(resourceFile => resourceFile.is_embeddable)
                    }
                )
                .catch(
                    (error) => console.error(error)
                )
        },
        redirectOnCreate (url = this.savepoint) {
            const logicCheck = (this.initialCourseView && this.course_id)
            if (logicCheck) window.location.replace(url)
        }
    },
    computed: {
        initialCourseView () {
            return (this.action === 'create')
        },
        savepoint () {
            let savepoint = (this.save_action === 'update') ? defaults.endpoints.update : defaults.endpoints.create
            return savepoint.replace(':id', this.course_id)
        },
        save_label () {
            return (this.save_action === 'update') ? this.labels.save : this.labels.create
        },
        mappedStatus () {
            return (this.course_status === defaults.status.active)
                ? 'active'
                : 'inactive'
        }
    },
    created () {
        this.course_title = (this.labels.new_course_title && !this.title)
            ? this.labels.new_course_title
            : this.course_title
        this.course_sections = (this.sections.length === 0)
            ? defaults.sections
            : this.course_sections
    }
}
</script>
