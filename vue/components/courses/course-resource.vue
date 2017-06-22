<template src="./course-resource.html"></template>
<style module src="../module.css"></style>

<script>
export default {
    name: 'course-resource',
    props: {
        id: Number,
        template: String,
        instance: {
            type: Object,
            default: () => {
                return {
                    title: 'Unnamed Resource',
                }
            }
        },
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
            type: 'CourseResource',
            edittable: false
        }
    },
    methods: {
        edit () {
            this.edittable = !this.edittable
        },
        update () {
            this.edit()
        }
    },
    beforeMount () {
        this.instance.type = this.$data.type
    }
}
</script>
