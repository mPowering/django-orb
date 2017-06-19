<script>
export default {
    name: 'course-resource',
    props: {
        title: String,
        description: String,
        tags: Array,
        labels: {
            type: Object,
            default: () => {
                return {
                    edit_resource: 'Edit Section Resource',
                    save_resource: 'Save Section Resource'
                }
            }
        }
    },
    data () {
        return {
            resource_title: '',
            resource_description: '',
            resource_tags: []
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
  <div class="course-resource">
    <h5>Unnamed Resource</h5>
  </div>
</template>

