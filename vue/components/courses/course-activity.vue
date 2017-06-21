<script>
export default {
    name: 'course-activity',
    props: {
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
            // this.$emit('update', this.activity)
            this.edit()
        }
    },
    // watch: {
    //     title () {
    //         this.activity_title = this.title
    //     }
    // },
    beforeMount () {}
}
</script>

<template>
  <div class="course-activity">
    <template v-if="edittable">
        <input class="form-control" v-model="instance.title">
        <textarea class="form-control" v-model="instance.description">
        </textarea>
        <button class="btn btn-success" type="button" @click="update">Save</button>
    </template>
    <template v-else>
        <h5 v-text="instance.title"></h5>
        <div v-text="instance.description"></div>
        <button class="btn btn-primary" type="button" @click="edit">Edit</button>
        <slot name="resource-footer-controls"></slot>
    </template>
    
  </div>
</template>

