<script>
import CourseResource from '@/courses/course-resource'
import draggable from 'vuedraggable'

export default {
    name: 'course-section',
    components: {
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
        addResource () {
            this.course_resources.push(
                {
                    title: 'Unnamed Text Slide'
                }
            )
        },
        removeResource (id) {
            this.course_resources = this.course_resources.filter(
                (section, index) => {
                    return index !== id
                }
            )
        },
    },
    beforeMount () {
        this.course_resources = (this.resources && this.resources instanceof Array)
            ? this.resources
            : this.course_resources
    }
}
</script>

<template>
  <div class="course-section">
    <div class="well list-group">
        <draggable :list="course_resources" :options="{group:'resources'}">
            <course-resource
                class="list-group-item"
                v-for="resource, index in course_resources"
                :key="resource"
                :title="resource.title"
            >
                <button class="btn btn-warning" @click="removeResource(index)">Remove Resource</button>
            </course-resource>
        </draggable>
    </div>
    <button class="btn btn-primary" v-text="labels.add_resource" @click="addResource"></button>
    <slot></slot>
  </div>
</template>
