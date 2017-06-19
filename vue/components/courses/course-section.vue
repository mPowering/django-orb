<script>
import CourseResource from '@/courses/course-resource'

export default {
    name: 'course-section',
    components: {
        CourseResource
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
        addResource () { this.course_resources.push([]) }
    },
    beforeMount () {
        this.course_resources = (this.resources && this.resources instanceof Array) ? this.resources : this.course_resources
    }
}
</script>

<template>
  <div class="course-section">
    <ul class="well list-group">
        <li class="list-group-item" v-for="resource in course_resources">
            <course-resource></course-resource>
        </li>
    </ul>
    <button v-text="labels.add_resource" @click="addResource"></button>
  </div>
</template>
