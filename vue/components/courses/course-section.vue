<template src="./course-section.html"></template>
<style module src="../module.css"></style>

<script>
import CourseResource from '@/courses/course-resource'
import CourseActivity from '@/courses/course-activity'
import draggable from 'vuedraggable'

export default {
    name: 'course-section',
    components: {
        CourseActivity,
        CourseResource,
        draggable
    },
    props: {
        resources: Array,
        labels: {
            type: Object,
            default: () => {
                return {
                    add_resource: 'Add Section Resource'
                }
            }
        }
    },
    data () {
        return {
            course_resources: [],
        }
    },
    methods: {
        addActivity () {
            this.course_resources.push(
                {
                    type: 'CourseActivity',
                    title: 'Unnamed Text Activity'
                }
            )
        },
        removeResource (id) {
            this.course_resources = this.course_resources.filter(
                (section, index) => {
                    return index !== id
                }
            )
        }
    },
    beforeMount () {
        this.course_resources = (this.resources && this.resources instanceof Array)
            ? this.resources
            : this.course_resources
    }
}
</script>
