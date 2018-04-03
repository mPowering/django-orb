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
        instance: {
            type: Object,
            default: () => ({
                resources: []
            })
        },
        labels: {
            type: Object,
            default: () => ({
                add_resource: 'Add Section Resource'
            })
        }
    },
    data () {
        return {}
    },
    methods: {
        addActivity () {
            this.instance.resources.push(
                {
                    type: 'CourseActivity',
                    title: 'Unnamed Text Activity'
                }
            )
        },
        removeResource (id) {
            this.instance.resources = this.instance.resources.filter(
                (section, index) => {
                    return index !== id
                }
            )
        }
    },
    beforeMount () { }
}
</script>

<style module src="../module.css"></style>
<template src="./course-section.html"></template>

