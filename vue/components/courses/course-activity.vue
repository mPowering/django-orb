<template src="./course-activity.html"></template>
<style module src="../module.css"></style>

<script>
export default {
    name: 'course-activity',
    props: {
        id: Number,
        instance: {
            type: Object,
            default: () => {
                return {
                    title: 'Unnamed Course Activity',
                    description: ''
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
    beforeMount () {}
}
</script>

