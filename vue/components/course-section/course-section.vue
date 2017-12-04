<template src="./course-section.html"></template>
<style module src="../module.css"></style>

<script>
import CourseResource from '@cmp/course-resource/course-resource'
import CourseActivity from '@cmp/course-activity/course-activity'
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
