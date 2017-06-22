<script>
export default {
    name: 'course-resource',
    props: {
        instance: {
            type: Object,
            default: () => {
                return {
                    title: 'Unnamed Course Activity',
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
    },
    beforeMount () {}
}
</script>

<template>
    <div class="course-resource">
        <h5 v-text="instance.title"></h5>
        <slot name="resource-footer-controls"></slot>
    </div>
</template>

