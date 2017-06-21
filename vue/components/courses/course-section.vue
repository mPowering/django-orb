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
        // updateResource (obj) {
        //     console.log(obj)
        // }
        // @update="updateResource"
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
            <!-- can be CourseActivity or CourseResource -->
            <component
                :is="resource.type"
                class="list-group-item"
                v-for="resource, index in course_resources"
                :key="resource"
                :instance="resource"
                
            >
                <button slot="resource-footer-controls" class="btn btn-warning" @click="removeResource(index)">Remove Resource</button>
            </component>
        </draggable>
    </div>
    <button class="btn btn-primary" v-text="labels.add_activity" @click="addActivity"></button>
    <slot name="section-footer-controls"></slot>
  </div>
</template>
